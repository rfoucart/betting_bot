import pandas as pd
import datetime
from pandas.testing import assert_frame_equal
from tools import filters


class TestFilters:
    def test_filter_by_category_with_matching_category(self):
        data = {
            'Catégorie': ['boosts', 'values', 'boosts'],
            'Value': [1, 2, 3]
        }
        df = pd.DataFrame(data)
        category = 'boosts'
        result = filters.filter_by_category(df, category)
        result.reset_index(drop=True, inplace=True)
        expected_data = {
            'Catégorie': ['boosts', 'boosts'],
            'Value': [1, 3]
        }
        expected_df = pd.DataFrame(expected_data)
        assert_frame_equal(result, expected_df)

    def test_filter_by_category_with_no_matching_category(self):
        data = {
            'Catégorie': ['boosts', 'values', 'boosts'],
            'Value': [1, 2, 3]
        }
        df = pd.DataFrame(data)
        category = 'other'
        result = filters.filter_by_category(df, category)
        assert result.empty

    def test_filter_by_date_with_valid_dates(self):
        data = {
            'Date': ['01/01/2022 10:00', '02/01/2022 10:00', '03/01/2022 10:00'],
            'Value': [1, 2, 3]
        }
        df = pd.DataFrame(data)
        start_date = datetime.datetime(2022, 1, 2)
        end_date = datetime.datetime(2022, 1, 3)
        result = filters.filter_by_date(df, start_date, end_date, False)
        result.reset_index(drop=True, inplace=True)

        expected_data = {
            'Date': ['02/01/2022 10:00'],
            'Value': [2]
        }
        expected_df = pd.DataFrame(expected_data)
        expected_df['Date'] = pd.to_datetime(expected_df['Date'], dayfirst=True)  # Convert 'Date' column to datetime
        assert_frame_equal(result, expected_df)

    def test_filter_by_date_with_no_matching_dates(self):
        data = {
            'Date': ['01/01/2022 10:00', '02/01/2022 10:00', '03/01/2022 10:00'],
            'Value': [1, 2, 3]
        }
        df = pd.DataFrame(data)
        start_date = datetime.datetime(2023, 1, 2)
        end_date = datetime.datetime(2023, 1, 3)
        result = filters.filter_by_date(df, start_date, end_date, False)
        assert result.empty

    def test_filter_by_date_with_sorting(self):
        data = {
            'Date': ['03/01/2022 10:00', '01/01/2022 10:00', '02/01/2022 10:00'],
            'Value': [3, 1, 2]
        }
        df = pd.DataFrame(data)
        start_date = datetime.datetime(2022, 1, 1)
        end_date = datetime.datetime(2022, 1, 4)
        result = filters.filter_by_date(df, start_date, end_date, True)
        result.reset_index(drop=True, inplace=True)
        expected_data = {
            'Date': ['01/01/2022 10:00', '02/01/2022 10:00', '03/01/2022 10:00'],
            'Value': [1, 2, 3]
        }
        expected_df = pd.DataFrame(expected_data)
        expected_df['Date'] = pd.to_datetime(expected_df['Date'], dayfirst=True)  # Convert 'Date' column to datetime
        assert_frame_equal(result, expected_df)
