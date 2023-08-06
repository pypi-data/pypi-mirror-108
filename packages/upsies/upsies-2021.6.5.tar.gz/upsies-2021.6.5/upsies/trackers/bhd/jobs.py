"""
:class:`~.base.TrackerJobsBase` subclass
"""

import asyncio
import builtins
import os
import re

import unidecode

from ... import (__homepage__, __project_name__, __version__, constants,
                 errors, jobs)
from ...utils import (as_groups, cached_property, fs, http, image, release,
                      string, timestamp, video, webdbs)
from ..base import TrackerJobsBase

import logging  # isort:skip
_log = logging.getLogger(__name__)


class BhdTrackerJobs(TrackerJobsBase):
    @cached_property
    def guessed_release_name(self):
        return release.ReleaseName(self.content_path)

    @cached_property
    def approved_release_name(self):
        if self.release_name_job.is_finished:
            release_name = self.get_job_output(self.release_name_job, slice=0)
            return release.ReleaseName(release_name)
        else:
            raise RuntimeError('release_name_job must be finished')

    movie_types = (release.ReleaseType.movie,)
    series_types = (release.ReleaseType.season, release.ReleaseType.episode)

    @cached_property
    def jobs_before_upload(self):
        return (
            # Interactive jobs
            self.category_job,
            self.imdb_job,
            self.tmdb_job,
            self.release_name_job,
            self.type_job,
            self.source_job,
            self.description_job,

            # Background jobs
            # self.create_torrent_job,
            self.mediainfo_job,
            self.screenshots_job,
            self.upload_screenshots_job,
            # self.scene_check_job,

        )

    # How many screenshots to make
    screenshots = 4

    @cached_property
    def category_job(self):
        return self.make_choice_job(
            name='category',
            label='Category',
            autodetected=self.guessed_release_name.type,
            autofinish=False,
            options=(
                {'label': 'Movie', 'value': 1, 'match': lambda t: t in self.movie_types},
                {'label': 'TV', 'value': 2, 'match': lambda t: t in self.series_types},
            ),
        )

    @cached_property
    def type_job(self):
        self.release_name_job.signal.register('finished', self.autodetect_type)
        return self.make_choice_job(
            name='type',
            label='Type',
            autodetected=self.guessed_release_name,
            autofinish=False,
            options=(
                {'label': 'UHD 100', 'value': 'UHD 100'},
                {'label': 'UHD 66', 'value': 'UHD 66'},
                {'label': 'UHD 50', 'value': 'UHD 50'},
                {'label': 'UHD Remux', 'value': 'UHD Remux'},
                {'label': 'BD 50', 'value': 'BD 50'},
                {'label': 'BD 25', 'value': 'BD 25'},
                {'label': 'BD Remux', 'value': 'BD Remux'},
                {'label': '2160p', 'value': '2160p'},
                {'label': '1080p', 'value': '1080p'},
                {'label': '1080i', 'value': '1080i'},
                {'label': '720p', 'value': '720p'},
                {'label': '576p', 'value': '576p'},
                {'label': '540p', 'value': '540p'},
                {'label': 'DVD 9', 'value': 'DVD 9'},
                {'label': 'DVD 5', 'value': 'DVD 5'},
                {'label': 'DVD Remux', 'value': 'DVD Remux'},
                {'label': '480p', 'value': '480p'},
                {'label': 'Other', 'value': 'Other'},
            ),
        )

    def autodetect_type(self, release_name_job):
        approved_resolution = self.approved_release_name.resolution
        approved_source = self.approved_release_name.source
        _log.debug('Approved resolution: %r', approved_resolution)
        _log.debug('Approved source: %r', approved_source)
        if approved_source == 'DVD9':
            self.type_job.focused = 'DVD 9'
        elif approved_source == 'DVD5':
            self.type_job.focused = 'DVD 5'
        elif approved_source == 'DVD Remux':
            self.type_job.focused = 'DVD Remux'
        elif approved_resolution == '2160p':
            self.type_job.focused = '2160p'
        elif approved_resolution == '1080p':
            self.type_job.focused = '1080p'
        elif approved_resolution == '1080i':
            self.type_job.focused = '1080i'
        elif approved_resolution == '720p':
            self.type_job.focused = '720p'
        elif approved_resolution == '576p':
            self.type_job.focused = '576p'
        elif approved_resolution == '540p':
            self.type_job.focused = '540p'
        elif approved_resolution == '480p':
            self.type_job.focused = '480p'

    @cached_property
    def source_job(self):
        self.release_name_job.signal.register('finished', self.autodetect_source)
        return self.make_choice_job(
            name='source',
            label='Source',
            autodetected=self.guessed_release_name.source,
            autofinish=False,
            options=(
                {'label': 'Blu-ray', 'value': 'Blu-ray'},
                {'label': 'HD-DVD', 'value': 'HD-DVD'},
                {'label': 'WEB', 'value': 'WEB'},
                {'label': 'HDTV', 'value': 'HDTV'},
                {'label': 'DVD', 'value': 'DVD'},
            ),
        )

    # Map source_job labels to regular expressions
    source_regexs = {
        'Blu-ray': re.compile(r'BluRay'),
        'HD-DVD': re.compile(r'HD-DVD'),
        'WEB': re.compile(r'(?:WEBRip|WEB-DL)'),
        'HDTV': re.compile(r'HDTV'),
        'DVD': re.compile(r'DVD'),
    }

    def autodetect_source(self, release_name_job):
        approved_source = self.approved_release_name.source
        for label, regex in self.source_regexs.items():
            if regex.match(approved_source):
                self.source_job.focused = label

    @cached_property
    def description_job(self):
        job = jobs.dialog.TextFieldJob(
            name='description',
            label='Description',
            read_only=True,
            **self.common_job_args,
        )
        job.add_task(
            job.fetch_text(
                coro=self.generate_screenshots_bbcode(),
                finish_on_success=True,
            )
        )
        return job

    async def generate_screenshots_bbcode(self):
        # Wait until all screenshots are uploaded
        await self.upload_screenshots_job.wait()
        rows = []
        screenshot_groups = as_groups(
            self.upload_screenshots_job.uploaded_images,
            group_sizes=(2, 3),
            default='MISSING SCREENSHOT',
        )
        for screenshots in screenshot_groups:
            cells = []
            for screenshot in screenshots:
                cells.append(f'[url={screenshot}][img]{screenshot.thumbnail_url}[/img][/url]')
            # Space between columns
            rows.append(' '.join(cells))
        # Empty line between rows
        bbcode = '\n\n'.join(rows)
        return f'[center]\n{bbcode}\n[/center]'

    @property
    def post_data(self):
        return {
            'name': self.get_job_output(self.release_name_job, slice=0),
            'category_id': self.get_job_attribute(self.category_job, 'choice'),
            'type': self.get_job_attribute(self.type_job, 'choice'),
            'source': self.get_job_attribute(self.source_job, 'choice'),
    	    'imdb_id': self.get_job_output(self.imdb_job, slice=0),
    	    'tmdb_id': self.get_job_output(self.tmdb_job, slice=0).split('/')[1],
            'mediainfo': self.get_job_output(self.mediainfo_job, slice=0),
            'description': self.get_job_output(self.description_job, slice=0),
            'anon': '1' if self.options['anonymous'] else '0',
            'pack': self.post_data_pack,
            'sd': self.post_data_sd,
            'live': '0' if self.options['draft'] else '1',
        }

    @property
    def post_data_pack(self):
        if self.approved_release_name.type is release.ReleaseType.season:
            return '1'
        else:
            return '0'

    @property
    def post_data_sd(self):
        try:
            height = int(self.approved_release_name.resolution[:-1])
        except ValueError:
            return '0'
        else:
            return '1' if height < 720 else '0'

# edition	string	The edition of the uploaded release. (Collector, Director, Extended, Limited, Special, Theatrical, Uncut or Unrated)
# custom_edition 	string	A custom edition like 'The Final Cut' for Blade Runner.
# region	string	The region in which the disc was released. Only for discs! (AUS, CAN, CEE, CHN, ESP, EUR, FRA, GBR, GER, HKG, ITA, JPN, KOR, NOR, NLD, RUS, TWN or USA)
# tags	string	Any additional tags separated by comma(s). (Commentary, 2in1, Hybrid, OpenMatte, 2D3D, WEBRip, WEBDL, 3D, 4kRemaster, DualAudio, EnglishDub, Personal, Scene, DigitalExtras, Extras)
# nfo	string	The NFO of the torrent as string.
# nfo_file	file	The NFO of the torrent as file.
