import unittest
import json
from url_shortner import app, url_map

url_map['abc123'] = {
    'short_code': 'abc123',
    'url': 'http://example.com',
    'created': '2022-03-24 12:00:00',
    'redirect_count': 0,
    'last_redirect': ''
}


class shorten_url_test_case(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.url = '/shorten'
        self.payload = {"url": "https://www.try.com", "shortcode": 'abc123'}
        self.response = self.app.post(self.url, json=self.payload)

    def tearDown(self):
        url_map.clear()

    def test_shorten_url_status_code(self):
        try:
            self.assertEqual(self.response.status_code, 201)
            print("Shorten_Url: Status code tested successfully")
        except Exception as e:
            print("Error: ", e)

    def test_shorten_url_content_type(self):
        try:
            self.assertIn('application/json', self.response.content_type)
            print("Shorten Url: Content type tested successfully")
        except Exception as e:
            print("Error: ", e)

    def test_shorten_url_data(self):
        try:
            response_data = json.loads(self.response.data)
            expected_data = {'shortcode': 'abc123'}
            self.assertEqual(response_data, expected_data)
            print("Shorten Url: Data tested successfully")
        except Exception as e:
            print("Error: ", e)


class extract_url_test_case(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.url = '/abc123'
        self.response = self.app.get(self.url)

    def test_extract_url_status_code(self):
        try:
            statuscode = self.response.status_code
            self.assertEqual(statuscode, 302)
            print("Extract_Url: Status code tested successfully")
        except Exception as e:
            print("Error: ", e)

    def test_extract_url_content_type(self):
        try:
            content_type = self.response.headers.get('Content-Type', '')
            self.assertIn('application/json', content_type)
            print("Extract Url: Content type tested successfully")
        except Exception as e:
            print("Error: ", e)

    def test_extract_url_data(self):
        try:
            response_data = json.loads(self.response.data)
            expected_data = {'location': 'http://example.com'}
            self.assertEqual(response_data, expected_data)
            print("Extract Url: Data tested successfully")
        except Exception as e:
            print("Error: ", e)


class get_stats_test_case(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.url = '/abc123/stats'
        self.response = self.app.get(self.url)

    def test_get_stats_status_code(self):
        try:
            self.assertEqual(self.response.status_code, 200)
            print("Get_Stats: Status code tested successfully")
        except Exception as e:
            print("Error: ", e)

    def test_get_stats_content_type(self):
        try:
            content_type = self.response.headers.get('Content-Type', '')
            self.assertIn('application/json', content_type)
            print("Get Stats: Content type tested successfully")
        except Exception as e:
            print("Error: ", e)

    def test_get_stats_keys_returned(self):
        try:
            response_data = json.loads(self.response.data)
            self.assertIn('last_redirect', response_data)
            self.assertIn('redirect_count', response_data)
            self.assertIn('created', response_data)
            print("Get Stats: Keys tested successfully")
        except Exception as e:
            print("Error: ", e)

    def test_get_stats_returned_value_types(self):
        try:
            response_data = json.loads(self.response.data)
            self.assertIsInstance(response_data['created'], str)
            self.assertIsInstance(response_data['redirect_count'], int)
            self.assertIsInstance(response_data['last_redirect'], str)
            print("Get Stats: Value type tested successfully")
        except Exception as e:
            print("Error: ", e)


if __name__ == '__main__':
    unittest.main()
