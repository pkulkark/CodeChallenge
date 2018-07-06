import sys
sys.path.insert(0, '/home/pooja/CodeChallenge/list-paginated-data/src')

import paginate
import unittest

from mock import patch


class PaginatedDataTest(unittest.TestCase):
    def setUp(self):
        self.verfied_user = "TestUser1"

    def test_hashing_password(self):
        password = "TestPasswd1"
        hash_pass = paginate._hash_password(password)
        self.assertNotEqual(password, hash_pass)
        self.assertNotEqual(len(password), len(hash_pass))

    @patch('paginate._fetch_user')
    def test_auth_token_generation(self, mock_fetch_user):
        mock_fetch_user.return_value = ('1', self.verfied_user, 'somepass')
        auth_token = paginate._generate_auth_token(self.verfied_user)
        user = paginate._verify_auth_token(auth_token)
        self.assertEqual(user, "TestUser1")

    @patch('paginate._fetch_user')
    def test_verify_auth_token(self, mock_fetch_user):
        mock_fetch_user.return_value = ('1', self.verfied_user, 'somepass')
        auth_token = paginate._generate_auth_token(self.verfied_user)
        auth_token = auth_token[:5]
        user = paginate._verify_auth_token(auth_token)
        self.assertEqual(user, None)
        


if __name__ == '__main__':
    unittest.main()
