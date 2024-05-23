from datetime import datetime

import pytest

from tools.utils import get_date_bounds, list_to_str


class TestGetDateBounds:
    def test_get_date_bounds_for_one_day(self):
        start_date, end_date = get_date_bounds("010121", 1)
        assert start_date == datetime(2021, 1, 1, 6, 0)
        assert end_date == datetime(2021, 1, 2, 6, 0)

    def test_date_bounds_for_multiple_days(self):
        start_date, end_date = get_date_bounds("010122", 3)
        assert start_date == datetime(2022, 1, 1, 6, 0)
        assert end_date == datetime(2022, 1, 4, 6, 0)

    def test_date_bounds_for_zero_days(self):
        start_date, end_date = get_date_bounds("010122", 0)
        assert start_date == datetime(2022, 1, 1, 6, 0)
        assert end_date == datetime(2022, 1, 1, 6, 0)

    def test_date_bounds_for_negative_days(self):
        with pytest.raises(ValueError):
            get_date_bounds("010122", -1)


class TestListToStrTests:
    def test_converts_list_to_string_with_default_separator(self):
        result = list_to_str(['Hello', 'World'])
        assert result == 'Hello\nWorld'

    def test_converts_list_to_string_with_custom_separator(self):
        result = list_to_str(['Hello', 'World'], ', ')
        assert result == 'Hello, World'

    def test_converts_empty_list_to_empty_string(self):
        result = list_to_str([])
        assert result == ''

    def test_converts_list_with_single_element(self):
        result = list_to_str(['Hello'])
        assert result == 'Hello'
