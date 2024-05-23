import pytest
from classes.bet_odds import BetOdds


class TestBetOddsWithTwoValues:
    @pytest.fixture
    def bet_odds(self):
        return BetOdds((1.8, 1.9))

    def test_odds_are_set_correctly(self, bet_odds):
        assert bet_odds.odds == (1.8, 1.9)

    def test_margin_is_computed_correctly(self, bet_odds):
        assert pytest.approx(bet_odds.margin, abs=1e-5) == 0.07567

    def test_true_odds_are_computed_correctly(self, bet_odds):
        assert pytest.approx(bet_odds.odds_without_margin, abs=1e-4) == (1.9316, 2.0472)

    def test_true_probabilities_are_computed_correctly(self, bet_odds):
        assert pytest.approx(bet_odds.true_probs, abs=1e-4) == (0.5177, 0.4885)

    def test_odds_setter_rejects_non_tuple(self, bet_odds):
        with pytest.raises(TypeError):
            bet_odds.odds = [1.8, 1.9]

    def test_odds_setter_rejects_values_less_than_one(self, bet_odds):
        with pytest.raises(ValueError):
            bet_odds.odds = (0.5, 4.0)


class TestBetOddsWithThreeValues:
    @pytest.fixture
    def bet_odds(self):
        return BetOdds((2.45, 3.0, 3.2))

    def test_odds_are_set_correctly(self, bet_odds):
        assert bet_odds.odds == (2.45, 3.0, 3.2)

    def test_margin_is_computed_correctly(self, bet_odds):
        assert pytest.approx(bet_odds.margin, abs=1e-5) == 0.05123

    def test_true_odds_are_computed_correctly(self, bet_odds):
        assert pytest.approx(bet_odds.odds_without_margin, abs=1e-4) == (2.5570, 3.1620, 3.3850)

    def test_true_probabilities_are_computed_correctly(self, bet_odds):
        assert pytest.approx(bet_odds.true_probs, abs=1e-4) == (0.3911, 0.3163, 0.2954)

    def test_odds_setter_rejects_non_tuple(self, bet_odds):
        with pytest.raises(TypeError):
            bet_odds.odds = [2.45, 3.0, 3.2]

    def test_odds_setter_rejects_values_less_than_one(self, bet_odds):
        with pytest.raises(ValueError):
            bet_odds.odds = (0.5, 3.0, 4.0)
