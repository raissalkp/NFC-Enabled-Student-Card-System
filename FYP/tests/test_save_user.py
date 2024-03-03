import pytest
from unittest.mock import patch, MagicMock
from save_user import save_user


@patch('save_user.database_connection')
def test_save_user(MockDB):
    MockDB.insert_user = MagicMock(return_value=True)

    result = save_user("John Doe", "12345")
    assert result == True
    MockDB.insert_user.assert_called_with("John Doe", "12345")
