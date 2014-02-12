import unittest
import json

from .. import lxc_ui_agent


class TestScraper(unittest.TestCase):
    def setUp(self):
        self.app = lxc_ui_agent.app.test_client()

    def test_entry(self):
        expected = {
            "comments": 105,
            "comments_url": "https://news.ycombinator.com/item?id=6804440",
            "points": 210,
            "submitter": "citricsquid",
            "time_submitted": "6 hours ago",
            "title": "I Am Not Satoshi",
            "url": "http://blog.dustintrammell.com/2013/11/26/i-am-not-satoshi/"
        }

        rv = self.app.get('/')
        self.assertEqual(json.loads(rv.data)['stories'][1], expected)


if __name__ == '__main__':
    unittest.main()