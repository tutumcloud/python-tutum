import unittest
import urllib.parse

import mock
import requests

import tutum
from .fake_api import fake_resp
from tutum.api.base import send_request


class SendRequestTestCase(unittest.TestCase):
    @mock.patch('tutum.api.http.Request', return_value=requests.Request('GET', 'http://fake.com'))
    @mock.patch.object(tutum.api.http.Session, 'send')
    def test_http_send_request(self, mock_send, mock_Request):
        json_obj = {'key': 'value'}
        mock_send.return_value = fake_resp(lambda: (None, json_obj))
        self.assertRaises(tutum.TutumApiError, send_request, 'METHOD', 'path', data='data')
        headers = {'Content-Type': 'application/json', 'User-Agent': 'python-tutum/v%s' % tutum.__version__}
        headers.update(tutum.auth.get_auth_header())
        mock_Request.assert_called_with('METHOD', urllib.parse.urljoin(tutum.base_url, 'path/'),
                                        headers=headers, data='data')

        mock_send.return_value = fake_resp(lambda: (200, json_obj))
        self.assertEqual(json_obj, send_request('METHOD', 'path'))

        mock_send.return_value = fake_resp(lambda: (204, json_obj))
        self.assertIsNone(send_request('METHOD', 'path'))

        mock_send.return_value = fake_resp(lambda: (401, json_obj))
        self.assertRaises(tutum.TutumAuthError, send_request, 'METHOD', 'path')

        mock_send.return_value = fake_resp(lambda: (500, json_obj))
        self.assertRaises(tutum.TutumApiError, send_request, 'METHOD', 'path')