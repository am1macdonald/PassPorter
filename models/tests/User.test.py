import unittest
from unittest.mock import patch, MagicMock
from pydantic import EmailStr, SecretStr
from models.User import User

class UserTests(unittest.TestCase):
    @patch('models.User.DatabaseController')
    def user_creation_with_valid_email_and_password(self, mock_db):
        email = EmailStr('test@example.com')
        password = SecretStr('password123')
        user = User(email, password)
        self.assertEqual(user.email, email)
        self.assertIsNotNone(user.password)

    @patch('models.User.DatabaseController')
    def user_creation_without_password(self, mock_db):
        email = EmailStr('test@example.com')
        user = User(email)
        self.assertEqual(user.email, email)
        self.assertIsNone(user.password)

    @patch('models.User.DatabaseController')
    def add_user_to_database(self, mock_db):
        email = EmailStr('test@example.com')
        password = SecretStr('password123')
        user = User(email, password)
        user.add()
        mock_db.return_value.connect.assert_called_once()
        mock_db.return_value.insert.assert_called()
        mock_db.return_value.disconnect.assert_called_once()

    @patch('models.User.DatabaseController')
    def get_user_from_database(self, mock_db):
        email = EmailStr('test@example.com')
        password = SecretStr('password123')
        user = User(email, password)
        mock_db.return_value.arbitrary.return_value = [1, 'username', 'test@example.com', 'hashed_password', None, True, 0]
        db_user = user.get_user()
        mock_db.return_value.connect.assert_called_once()
        mock_db.return_value.arbitrary.assert_called()
        mock_db.return_value.disconnect.assert_called_once()
        self.assertEqual(db_user.email, email)

if __name__ == '__main__':
    unittest.main()
