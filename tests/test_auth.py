from __future__ import absolute_import
import tempfile
import unittest
import unittest.mock as mock
import os
import tutum
from .fake_api import *


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.tutum_auth = tutum.tutum_auth
        self.basic_auth = tutum.basic_auth

    def tearDown(self):
        tutum.tutum_auth = self.tutum_auth
        tutum.basic_auth = self.basic_auth

    def test_baseurl(self):
        self.assertTrue(tutum.base_url)

    @mock.patch('tutum.api.auth.verify_credential')
    def test_auth_authenticate(self, mock_verify_credential):
        tutum.auth.authenticate(FAKE_USER, FAKE_PASSWORD)
        mock_verify_credential.assert_called_with(FAKE_USER, FAKE_PASSWORD)
        self.assertEqual(tutum.basic_auth, FAKE_BASIC_AUTH)
        self.tearDown()

    def test_auth_is_authenticated(self):
        tutum.tutum_auth = FAKE_TUTUM_AUTH
        tutum.basic_auth = FAKE_BASIC_AUTH
        tutum.apikey_auth = FAKE_APIKEY_AUTH
        self.assertTrue(tutum.auth.is_authenticated())

        tutum.tutum_auth = None
        tutum.basic_auth = FAKE_BASIC_AUTH
        tutum.apikey_auth = None
        self.assertTrue(tutum.auth.is_authenticated())

        tutum.tutum_auth = FAKE_TUTUM_AUTH
        tutum.basic_auth = None
        tutum.apikey_auth = None
        self.assertTrue(tutum.auth.is_authenticated())

        tutum.tutum_auth = None
        tutum.basic_auth = None
        tutum.apikey_auth = FAKE_APIKEY_AUTH
        self.assertTrue(tutum.auth.is_authenticated())

        tutum.tutum_auth = None
        tutum.basic_auth = None
        tutum.apikey_auth = None
        self.assertFalse(tutum.auth.is_authenticated())

    def test_auth_logout(self):
        tutum.tutum_auth = FAKE_TUTUM_AUTH
        tutum.basic_auth = FAKE_BASIC_AUTH
        tutum.apikey_auth = FAKE_APIKEY_AUTH
        tutum.auth.logout()
        self.assertIsNone(tutum.tutum_auth)
        self.assertIsNone(tutum.basic_auth)
        self.assertIsNone(tutum.apikey_auth)

    def test_auth_load_from_file(self):
        file = tempfile.NamedTemporaryFile('w', delete=False)
        with file as f:
            f.writelines(["[auth]\n", "user = %s\n" % FAKE_USER, "apikey = %s\n" % FAKE_APIKEY,
                          "basic_auth = %s\n" % FAKE_BASIC_AUTH])
        basic_auth, apikey_auth = tutum.auth.load_from_file(file.name)
        self.assertEqual(basic_auth, FAKE_BASIC_AUTH)
        self.assertEqual(apikey_auth, "%s:%s" % (FAKE_USER, FAKE_APIKEY))
        os.remove(file.name)

    def test_auth_load_from_file_with_exception(self):
        basic_auth, apikey_auth = tutum.auth.load_from_file('abc')
        self.assertIsNone(basic_auth)
        self.assertIsNone(apikey_auth)

    def test_auth_get_auth_header(self):
        tutum.tutum_auth = FAKE_TUTUM_AUTH
        tutum.basic_auth = FAKE_BASIC_AUTH
        tutum.apikey_auth = FAKE_APIKEY_AUTH
        self.assertEqual({'Authorization': FAKE_TUTUM_AUTH}, tutum.auth.get_auth_header())

        tutum.tutum_auth = None
        tutum.basic_auth = FAKE_BASIC_AUTH
        tutum.apikey_auth = FAKE_APIKEY_AUTH
        self.assertEqual({'Authorization': 'Apikey %s' % (tutum.apikey_auth)}, tutum.auth.get_auth_header())

        tutum.tutum_auth = None
        tutum.basic_auth = FAKE_BASIC_AUTH
        tutum.apikey_auth = None
        self.assertEqual({'Authorization': 'Basic %s' % (FAKE_BASIC_AUTH)}, tutum.auth.get_auth_header())

        tutum.tutum_auth = FAKE_TUTUM_AUTH
        tutum.basic_auth = None
        tutum.apikey_auth = FAKE_APIKEY_AUTH
        self.assertEqual({'Authorization': FAKE_TUTUM_AUTH}, tutum.auth.get_auth_header())

        tutum.tutum_auth = None
        tutum.basic_auth = None
        tutum.apikey_auth = None
        self.assertEqual({}, tutum.auth.get_auth_header())
