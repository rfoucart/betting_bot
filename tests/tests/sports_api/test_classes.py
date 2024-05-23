import pytest
from unittest.mock import patch
from sports_api.classes import BasketballAPI


class TestBasketballAPI:
    @patch('requests.get')
    def test_retrieves_nba_match_dates(self, mock_get):
        mock_get.return_value.text = """
        {
            "response": [
                {
                    "date": "2023-12-01T20:00:00Z",
                    "teams": {
                        "home": {"name": "Lakers"},
                        "away": {"name": "Warriors"}
                    }
                },
                {
                    "date": "2023-12-01T22:00:00Z",
                    "teams": {
                        "home": {"name": "Bulls"},
                        "away": {"name": "Heat"}
                    }
                }
            ]
        }
        """
        result = BasketballAPI.get_nba_match_dates("2023-12-01")
        assert len(result) == 2
        assert result[0]['name'] == 'Lakers - Warriors'
        assert result[1]['name'] == 'Bulls - Heat'

    @patch('requests.get')
    def test_retrieves_no_nba_match_dates(self, mock_get):
        mock_get.return_value.text = '{"response": []}'
        result = BasketballAPI.get_nba_match_dates("2023-12-01")
        assert len(result) == 0

    @patch('requests.get')
    def test_handles_api_error(self, mock_get):
        mock_get.return_value.text = '{"message": "API Error"}'
        with pytest.raises(Exception):
            BasketballAPI.get_nba_match_dates("2023-12-01")

    @patch('requests.get')
    def test_retrieve_matches_with_same_date_and_hour(self, mock_get):
        mock_get.return_value.text = """
        {
            "response": [
                {
                    "date": "2023-12-01T20:00:00Z",
                    "teams": {
                        "home": {"name": "Lakers"},
                        "away": {"name": "Warriors"}
                    }
                },
                {
                    "date": "2023-12-01T20:00:00Z",
                    "teams": {
                        "home": {"name": "Bulls"},
                        "away": {"name": "Heat"}
                    }
                }
            ]
        }
        """
        result = BasketballAPI.get_nba_match_dates("2023-12-01")
        assert result[0]['year'] == result[1]['year']
        assert result[0]['month'] == result[1]['month']
        assert result[0]['day'] == result[1]['day']
        assert result[0]['hour'] == result[1]['hour']
        assert result[0]['minute'] == '00'
        assert result[1]['minute'] == '01'

    @patch('requests.get')
    def test_retrieve_matches_with_different_hours(self, mock_get):
        mock_get.return_value.text = """
            {
                "response": [
                    {
                        "date": "2023-12-01T20:00:00Z",
                        "teams": {
                            "home": {"name": "Lakers"},
                            "away": {"name": "Warriors"}
                        }
                    },
                    {
                        "date": "2023-12-01T21:00:00Z",
                        "teams": {
                            "home": {"name": "Bulls"},
                            "away": {"name": "Heat"}
                        }
                    }
                ]
            }
            """
        result = BasketballAPI.get_nba_match_dates("2023-12-01")
        assert result[0]['year'] == result[1]['year']
        assert result[0]['month'] == result[1]['month']
        assert result[0]['day'] == result[1]['day']
        assert int(result[0]['hour']) == int(result[1]['hour']) - 1
        assert result[0]['minute'] == result[1]['minute']
