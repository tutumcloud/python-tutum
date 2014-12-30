import os
import tempfile
import unittest
import configparser

import unittest.mock as mock

import tutum
from .fake_api import *


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.user = tutum.user
        self.apikey = tutum.apikey

    def tearDown(self):
        tutum.user = self.user
        tutum.apikey = tutum.apikey

    def test_baseurl(self):
        self.assertTrue(tutum.base_url)


    @mock.patch('tutum.api.auth.get_auth')
    def test_auth_authenticate(self, mock_get_auth):
        mock_get_auth.return_value = (FAKE_USER, FAKE_APIKEY)
        tutum.auth.authenticate(FAKE_USER, FAKE_PASSWORD)
        self.assertEqual(FAKE_USER, tutum.user)
        self.assertEqual(FAKE_APIKEY, tutum.apikey)
        self.tearDown()

    @mock.patch.object(tutum.api.http.Session, 'send')
    def test_auth_get_auth(self, mock_send):
        mock_send.return_value = fake_resp(fake_auth)
        user, apikey = tutum.auth.get_auth(FAKE_USER, FAKE_PASSWORD)
        self.assertEqual(FAKE_USER, user)
        self.assertEqual(FAKE_APIKEY, apikey)


    def test_auth_is_authenticated(self):
        tutum.user = FAKE_USER
        tutum.apikey = FAKE_APIKEY
        self.assertTrue(tutum.auth.is_authenticated())

        tutum.user = None
        tutum.apikey = FAKE_APIKEY
        self.assertFalse(tutum.auth.is_authenticated())

        tutum.user = FAKE_USER
        tutum.apikey = None
        self.assertFalse(tutum.auth.is_authenticated())

        tutum.user = None
        tutum.apikey = None
        self.assertFalse(tutum.auth.is_authenticated())

    def test_auth_logout(self):
        tutum.user = FAKE_USER
        tutum.apikey = FAKE_APIKEY
        tutum.auth.logout()
        self.assertIsNone(tutum.user)
        self.assertIsNone(tutum.apikey)

    def test_auth_load_from_file(self):
        file = tempfile.NamedTemporaryFile(delete=False)
        with file as f:
            f.writelines(["[auth]\n", "user = %s\n" % FAKE_USER, "apikey = %s\n" % FAKE_APIKEY])
        user_read, apikey_read = tutum.auth.load_from_file(file.name)
        self.assertEqual(user_read, FAKE_USER)
        self.assertEqual(apikey_read, FAKE_APIKEY)
        os.remove(file.name)

    @mock.patch.object(tutum.auth.ConfigParser.ConfigParser, 'read', side_effect=configparser.Error)
    def test_auth_load_from_file_with_exception(self, mock_read):
        user_read, apikey_read = tutum.auth.load_from_file('abc')
        self.assertIsNone(user_read)
        self.assertIsNone(apikey_read)

    def test_auth_get_auth_header(self):
        tutum.user = FAKE_USER
        tutum.apikey = FAKE_APIKEY
        self.assertEqual({'Authorization': 'ApiKey %s:%s' % (FAKE_USER, FAKE_APIKEY)}, tutum.auth.get_auth_header())

        tutum.user = None
        tutum.apikey = FAKE_APIKEY
        self.assertEqual({}, tutum.auth.get_auth_header())

        tutum.user = FAKE_USER
        tutum.apikey = None
        self.assertEqual({}, tutum.auth.get_auth_header())

        tutum.user = None
        tutum.apikey = None
        self.assertEqual({}, tutum.auth.get_auth_header())
