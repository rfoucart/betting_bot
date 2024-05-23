import pandas as pd
import pytest
from unittest.mock import MagicMock
from pandas import DataFrame
from pandas.testing import assert_frame_equal

from classes.bet_odds import BetOdds
from classes.value_detector import ValueDetector


class TestValueDetectorTests:
    @pytest.fixture
    def mock_bookmaker_bet_odds(self):
        # Only the first odd has value in this example
        mock = MagicMock(spec=BetOdds)
        mock.odds = (2.55, 3.65, 2.65)
        return mock

    @pytest.fixture
    def mock_reference_bet_odds(self):
        mock = MagicMock(spec=BetOdds)
        mock.odds = (2.4, 3.75, 2.75)
        mock.margin = 0.04486251809
        mock.odds_without_margin = (2.4893, 3.9728, 2.8679)
        mock.true_probs = (0.4017, 0.2517, 0.3487)
        return mock

    def test_computes_values_correctly(self, mock_reference_bet_odds, mock_bookmaker_bet_odds):
        detector = ValueDetector()
        detector._compute_values(ref_odds=mock_reference_bet_odds, book_odds=mock_bookmaker_bet_odds)
        assert pytest.approx(detector._values, abs=1e-4) == (0.0244, -0.0812, -0.0760)

    def test_computes_kelly_criterion_correctly(self, mock_bookmaker_bet_odds):
        detector = ValueDetector()
        detector._values = (0.0244, -0.0812, -0.0760)
        detector._compute_kelly_criterion(mock_bookmaker_bet_odds)
        assert pytest.approx(detector._kelly, abs=1e-4) == (0.0157, -0.0307, -0.0461)

    def test_computes_estimated_stake_correctly(self, mock_bookmaker_bet_odds):
        detector = ValueDetector()
        detector._kelly = (0.0157, -0.0307, -0.0461)
        detector._compute_estimated_stake(mock_bookmaker_bet_odds)
        assert pytest.approx(detector._stakes, abs=1e-4) == (0.0062, -0.0084, -0.0174)

    def test_analyzes_correctly(self, mock_reference_bet_odds, mock_bookmaker_bet_odds):
        detector = ValueDetector()
        result = detector.analyze(mock_reference_bet_odds, mock_bookmaker_bet_odds, ("1", "N", "2"))
        expected_result = pd.DataFrame({
            "Result": ("1", "N", "2"),
            "FR_Odds": (2.55, 3.65, 2.65),
            "ps3838": (2.4, 3.75, 2.75),
            "True_Odds": (2.4893, 3.9728, 2.8679),
            "Probs": (0.4017, 0.2517, 0.3487),
            "Values": (0.0244, -0.0812, -0.0760),
            "Kelly": (0.0157, -0.0307, -0.0461),
            "Stakes": (0.0062, -0.0084, -0.0174)
        })
        assert_frame_equal(result, expected_result, check_dtype=False, check_exact=False, atol=1e-4)

    def test_cleans_dataframe_correctly(self):
        detector = ValueDetector()
        df = pd.DataFrame({
            "Result": ("1", "N", "2"),
            "FR_Odds": (2.55, 3.65, 2.65),
            "ps3838": (2.4, 3.75, 2.75),
            "True_Odds": (2.4893, 3.9728, 2.8679),
            "Probs": (0.4017, 0.2517, 0.3487),
            "Values": (0.0244, -0.0812, -0.0760),
            "Kelly": (0.0157, -0.0307, -0.0461),
            "Stakes": (0.0062, -0.0084, -0.0174)
        })
        cleaned_df = detector.clean_dataframe(df)
        expected_result = DataFrame({
            "Result": ("1", "N", "2"),
            "FR_Odds": (2.55, 3.65, 2.65),
            "ps3838": (2.4, 3.75, 2.75),
            "True_Odds": (2.49, 3.97, 2.87),
            "Probs": ("40.17%", "25.17%", "34.87%"),
            "Values": ("2.44%", "-8.12%", "-7.6%"),
            "Kelly": ("1.57%", "-3.07%", "-4.61%"),
            "Stakes": ("0.62%", "-0.84%", "-1.74%")
        })
        assert_frame_equal(cleaned_df, expected_result)
