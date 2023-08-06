"""
BhdTracker class
"""

from ... import errors
from ..base import TrackerBase
from .config import BhdTrackerConfig
from .jobs import BhdTrackerJobs

import logging  # isort:skip
_log = logging.getLogger(__name__)


class BhdTracker(TrackerBase):
    name = 'bhd'
    label = 'BHD'

    argument_definitions = {
        ('--draft',): {
            'help': 'Upload as draft',
            'action': 'store_true',
        },
    }

    TrackerConfig = BhdTrackerConfig
    TrackerJobs = BhdTrackerJobs

    async def login(self):
        pass

    @property
    def is_logged_in(self):
        return True

    async def logout(self):
        pass

    async def get_announce_url(self):
        return '/'.join((
            self.options['announce_url'].rstrip('/'),
            self.options['announce_passkey'],
        ))

    async def upload(self, tracker_jobs):
        upload_url = '/'.join((
            self.options['upload_url'].rstrip('/'),
            self.options['apikey'],
        ))
        _log.debug('Uploading to %r', upload_url)
        _log.debug('POST data: %r', tracker_jobs.post_data)

        # response = await http.post(
        #     url=upload_url,
        #     cache=False,
        #     user_agent=True,
        #     files={'file': (tracker_jobs.torrent_filepath, 'application/octet-stream')},
        #     data=tracker_jobs.post_data,
        # )

        # _log.debug('Upload response: %r', response)
        # _log.debug('Upload response headers: %r', response.headers)
        # _log.debug('Upload response JSON: %r', response.json())

        # return str(torrent_page_url)
