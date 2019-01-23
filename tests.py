import copy
import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

from protos import accounts_pb2
import app

DEFAULT_USERS = [
    {
        "id": "1",
        "name": "Administrator",
        "email": "admin@example.com",
        "password": "password"
    }
]

class TestAccounts(unittest.TestCase):

    def setUp(self):
        self.account_service = app.AccountServicer()

    @patch("app.USERS", copy.deepcopy(DEFAULT_USERS))
    def test_list_users(self):
        # mock_users = copy.deepcopy(DEFAULT_USERS)

        request = MagicMock()
        context = MagicMock()

        resp = self.account_service.List(request, context)

        self.assertEqual(len(resp.accounts), 1)
        self.assertEqual(len(app.USERS), 1)

    @patch("app.USERS", copy.deepcopy(DEFAULT_USERS))
    def test_add_user(self):
        # mock_users = copy.deepcopy(DEFAULT_USERS)

        account = MagicMock()
        account.name = "Jim Halpert"
        account.email = "jim.halpert@dundermifflin.com"
        request = MagicMock()
        request.account = account
        request.password = "password123"
        context = MagicMock()

        resp = self.account_service.Create(request, context)

        self.assertEqual(len(app.USERS), 2)

    @patch("app.USERS", copy.deepcopy(DEFAULT_USERS))
    def test_add_existing_user(self):
        account = MagicMock()
        account.name = "Administrator"
        account.email = "admin@example.com"
        request = MagicMock()
        request.account = account
        request.password = "password"
        context = MagicMock()

        resp = self.account_service.Create(request, context)

        self.assertEqual(len(app.USERS), 1)

    @patch("app.USERS", copy.deepcopy(DEFAULT_USERS))
    def test_update_user(self):
        account = MagicMock()
        account.name = "Michael Scott"
        account.email = "admin@example.com"
        request = MagicMock()
        request.id = "1"
        request.account = account
        request.password = "password"
        context = MagicMock()

        resp = self.account_service.Update(request, context)

        self.assertEqual(len(app.USERS), 1)
        self.assertEqual(app.USERS[0]["name"], "Michael Scott")

    @patch("app.USERS", copy.deepcopy(DEFAULT_USERS))
    def test_delete_user(self):
        request = MagicMock()
        request.id = "1"
        context = MagicMock()

        resp = self.account_service.Delete(request, context)

        self.assertEqual(len(app.USERS), 0)

    @patch("app.USERS", copy.deepcopy(DEFAULT_USERS))
    def test_delete_non_existing_user(self):
        request = MagicMock()
        request.id = "32"
        context = MagicMock()

        resp = self.account_service.Delete(request, context)

        self.assertEqual(len(app.USERS), 1)

if __name__ == '__main__':
    unittest.main()