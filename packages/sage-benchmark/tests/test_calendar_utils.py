"""Tests for calendar utility functions (date/time parsing and formatting)."""

import pytest
from sage_benchmark.benchmarks.calendar_scheduling.environment.utils import (
    parse_date,
    parse_time,
    time_to_minutes,
)


class TestParseDate:
    """Tests for parse_date function."""

    def test_iso_format(self):
        """Test ISO format (YYYY-MM-DD)."""
        assert parse_date("2024-01-15") == "2024-01-15"
        assert parse_date("2024-12-31") == "2024-12-31"

    def test_us_format_with_dashes(self):
        """Test US format with dashes (MM-DD-YYYY)."""
        assert parse_date("01-15-2024") == "2024-01-15"
        assert parse_date("12-31-2024") == "2024-12-31"

    def test_us_format_with_slashes(self):
        """Test US format with slashes (M/D/YYYY)."""
        assert parse_date("1/15/2024") == "2024-01-15"
        assert parse_date("12/31/2024") == "2024-12-31"

    def test_full_month_name(self):
        """Test full month name format (January 15, 2024)."""
        assert parse_date("January 15, 2024") == "2024-01-15"
        assert parse_date("December 31, 2024") == "2024-12-31"

    def test_abbreviated_month_name(self):
        """Test abbreviated month name format (Jan 15, 2024)."""
        assert parse_date("Jan 15, 2024") == "2024-01-15"
        assert parse_date("Dec 31, 2024") == "2024-12-31"

    def test_day_first_full_month(self):
        """Test day-first format with full month (15 January 2024)."""
        assert parse_date("15 January 2024") == "2024-01-15"
        assert parse_date("31 December 2024") == "2024-12-31"

    def test_day_first_abbreviated_month(self):
        """Test day-first format with abbreviated month (15 Jan 2024)."""
        assert parse_date("15 Jan 2024") == "2024-01-15"
        assert parse_date("31 Dec 2024") == "2024-12-31"

    def test_whitespace_handling(self):
        """Test that leading/trailing whitespace is handled."""
        assert parse_date("  2024-01-15  ") == "2024-01-15"
        assert parse_date("  January 15, 2024  ") == "2024-01-15"

    def test_invalid_date_raises_error(self):
        """Test that invalid date formats raise ValueError."""
        with pytest.raises(ValueError, match="Unable to parse date"):
            parse_date("invalid date")

        with pytest.raises(ValueError, match="Unable to parse date"):
            parse_date("2024/01/15")  # Wrong separator for ISO

        with pytest.raises(ValueError, match="Unable to parse date"):
            parse_date("15-01-2024")  # DD-MM-YYYY not supported


class TestParseTime:
    """Tests for parse_time function."""

    def test_24_hour_format(self):
        """Test 24-hour format (HH:MM)."""
        assert parse_time("14:00") == "14:00"
        assert parse_time("09:30") == "09:30"
        assert parse_time("0:00") == "00:00"
        assert parse_time("23:59") == "23:59"

    def test_military_time(self):
        """Test military time format (HHMM)."""
        assert parse_time("1400") == "14:00"
        assert parse_time("0930") == "09:30"
        assert parse_time("0000") == "00:00"
        assert parse_time("2359") == "23:59"

    def test_simple_am_pm(self):
        """Test simple AM/PM format (2pm)."""
        assert parse_time("2pm") == "14:00"
        assert parse_time("2PM") == "14:00"
        assert parse_time("9am") == "09:00"
        assert parse_time("9AM") == "09:00"
        assert parse_time("12pm") == "12:00"
        assert parse_time("12am") == "00:00"

    def test_am_pm_with_minutes(self):
        """Test AM/PM format with minutes (2:30pm)."""
        assert parse_time("2:30pm") == "14:30"
        assert parse_time("2:30PM") == "14:30"
        assert parse_time("9:15am") == "09:15"
        assert parse_time("12:30pm") == "12:30"
        assert parse_time("12:30am") == "00:30"

    def test_am_pm_with_space(self):
        """Test AM/PM format with space (2:30 pm)."""
        assert parse_time("2:30 pm") == "14:30"
        assert parse_time("2:30 PM") == "14:30"
        assert parse_time("9 am") == "09:00"

    def test_edge_cases_noon_midnight(self):
        """Test edge cases for noon and midnight."""
        # Noon
        assert parse_time("12pm") == "12:00"
        assert parse_time("12:00pm") == "12:00"

        # Midnight
        assert parse_time("12am") == "00:00"
        assert parse_time("12:00am") == "00:00"

    def test_whitespace_handling(self):
        """Test that leading/trailing whitespace is handled."""
        assert parse_time("  14:00  ") == "14:00"
        assert parse_time("  2pm  ") == "14:00"

    def test_invalid_time_raises_error(self):
        """Test that invalid time formats raise ValueError."""
        with pytest.raises(ValueError, match="Unable to parse time"):
            parse_time("invalid")

        with pytest.raises(ValueError, match="Unable to parse time"):
            parse_time("afternoon")  # Not a time format

        with pytest.raises(ValueError, match="Unable to parse time"):
            parse_time("two thirty")  # Not a time format

    def test_out_of_range_raises_error(self):
        """Test that out-of-range hours/minutes raise ValueError."""
        with pytest.raises(ValueError, match="Invalid hour"):
            parse_time("25:00")  # Hour out of range

        with pytest.raises(ValueError, match="Invalid hour"):
            parse_time("2500")  # Military time hour out of range

        with pytest.raises(ValueError, match="Invalid minutes"):
            parse_time("12:60")  # Minutes out of range

        with pytest.raises(ValueError, match="Invalid hour"):
            parse_time("13pm")  # Invalid 12-hour format

        with pytest.raises(ValueError, match="Invalid hour"):
            parse_time("0am")  # 0 is invalid for 12-hour format


class TestTimeToMinutes:
    """Tests for time_to_minutes function."""

    def test_midnight(self):
        """Test midnight conversion."""
        assert time_to_minutes("00:00") == 0

    def test_noon(self):
        """Test noon conversion."""
        assert time_to_minutes("12:00") == 720

    def test_end_of_day(self):
        """Test end of day conversion."""
        assert time_to_minutes("23:59") == 1439

    def test_various_times(self):
        """Test various time conversions."""
        assert time_to_minutes("09:30") == 570  # 9*60 + 30
        assert time_to_minutes("14:45") == 885  # 14*60 + 45
        assert time_to_minutes("01:00") == 60
