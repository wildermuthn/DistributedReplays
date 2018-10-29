import unittest
import requests

from tests.utils import get_complex_replay_list, download_replay_discord

LOCAL_URL = 'http://localhost:8000'

class RunningServerTest(unittest.TestCase):
    replay_status = []

    @classmethod
    def setUpClass(cls):
        pass
        # start_server()
        # cls.thread = Thread(target=start_server)
        # cls.thread.start()
        # for replay_url in get_complex_replay_list():
        #     cls.replay_status.append(
        #         requests.post('http://localhost:8000/api/upload', files={'file': download_replay_discord(replay_url)}))

    def test_replays_status(self):
        for replay_url in get_complex_replay_list()[:1]:
            print('Testing:', replay_url)
            requests.post(LOCAL_URL + '/api/upload', files={'file': download_replay_discord(replay_url)})

        print(self.replay_status)
