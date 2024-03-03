import pytest
from unittest.mock import patch, MagicMock
from check_attendance import check_attendance


@patch('check_attendance.attendance_database')
def test_check_attendance(MockDB):
    MockDB.get_attendance_record = MagicMock(return_value=["John Doe", "Jane Doe"])

    result = check_attendance("John Doe")
    assert result == True
    MockDB.get_attendance_record.assert_called_once()
