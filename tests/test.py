import os
import tempfile
import unittest
import tutum


class ConfigurationTestCase(unittest.TestCase):
    def test_baseurl(self):
        self.assertTrue(tutum.base_url is not None)

    def test_parse_ini_file(self):
        file = tempfile.NamedTemporaryFile(delete=False)
        with file as f:
            f.writelines(["[auth]\n", "user = testuser\n", "apikey = testapikey\n"])
        user_read, apikey_read = tutum.auth.load_from_file(file.name)
        self.assertEqual(user_read, "testuser")
        self.assertEqual(apikey_read, "testapikey")
        os.remove(file.name)