import unittest
from unittest.mock import patch, MagicMock

from DatabaseController import DatabaseController


class TestDatabaseController(unittest.TestCase):
    @patch('psycopg2.connect')
    def setUp(self, mock_connect):
        self.db_controller = DatabaseController()
        self.mock_cursor = MagicMock()
        self.mock_connection = MagicMock()
        self.mock_connection.cursor.return_value = self.mock_cursor
        mock_connect.return_value = self.mock_connection
        self.db_controller.cursor = self.mock_cursor
        self.db_controller.connection = self.mock_connection

    def test_insert_with_valid_data(self):
        self.mock_cursor.fetchone.return_value = True
        result = self.db_controller.insert('test_table', ['column1'], ('value1',))
        self.assertEqual(result, True)
        self.mock_cursor.execute.assert_called_once()
        self.mock_connection.commit.assert_called_once()

    def test_insert_with_invalid_data(self):
        self.mock_cursor.fetchone.return_value = None
        result = self.db_controller.insert('test_table', ['column1'], ('value1',))
        self.assertEqual(result, None)
        self.mock_cursor.execute.assert_called_once()
        self.mock_connection.rollback.assert_called_once()

    def test_select_with_wheres(self):
        self.mock_cursor.fetchall.return_value = [('value1',)]
        result = self.db_controller.select(['column1'], 'test_table', wheres=['column1=value1'])
        self.assertEqual(result, [('value1',)])
        self.mock_cursor.execute.assert_called_once()

    def test_select_without_wheres(self):
        self.mock_cursor.fetchall.return_value = [('value1',)]
        result = self.db_controller.select(['column1'], 'test_table')
        self.assertEqual(result, [('value1',)])
        self.mock_cursor.execute.assert_called_once()

    def test_disconnect_closes_cursor_and_connection(self):
        self.db_controller.disconnect()
        self.mock_cursor.close.assert_called_once()
        self.mock_connection.close.assert_called_once()


    def select_returns_correct_data_when_data_exists(self):
        self.mock_cursor.fetchall.return_value = [('value1',)]
        result = self.db_controller.select(['column1'], 'test_table')
        self.assertEqual(result, [('value1',)])
        self.mock_cursor.execute.assert_called_once()


    def select_returns_empty_list_when_no_data_exists(self):
        self.mock_cursor.fetchall.return_value = []
        result = self.db_controller.select(['column1'], 'test_table')
        self.assertEqual(result, [])
        self.mock_cursor.execute.assert_called_once()


if __name__ == '__main__':
    unittest.main()
