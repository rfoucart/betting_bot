import pandas as pd

from messages import NEGATIVE_BANKROLL_MESSAGE
from tools.writers import pending_bets_evaluation


class TestPendingBetsEvaluationTests:
    def test_evaluates_pending_bets_with_positive_profit(self):
        pending_bets = pd.DataFrame({
            'reworked_stakes': [10, 20],
            'Cote': [1.5, 2.0]
        })
        result = pending_bets_evaluation(pending_bets, 100, 10)
        assert result == 'Résultat final compris entre -20.0% et +35.0% (2 paris encore en cours)'

    def test_evaluates_pending_bets_with_negative_profit(self):
        pending_bets = pd.DataFrame({
            'reworked_stakes': [10, 20],
            'Cote': [1.5, 2.0]
        })
        result = pending_bets_evaluation(pending_bets, 100, -10)
        assert result == 'Résultat final compris entre -40.0% et +15.0% (2 paris encore en cours)'

    def test_evaluates_pending_bets_with_no_pending_bets(self):
        pending_bets = pd.DataFrame({
            'reworked_stakes': [],
            'Cote': []
        })
        result = pending_bets_evaluation(pending_bets, 100, 10)
        assert result == 'Résultat final compris entre +10.0% et +10.0% (0 pari encore en cours)'

    def test_evaluates_pending_bets_with_zero_bankroll(self):
        pending_bets = pd.DataFrame({
            'reworked_stakes': [10, 20],
            'Cote': [1.5, 2.0]
        })
        result = pending_bets_evaluation(pending_bets, 0, 10)
        assert result == NEGATIVE_BANKROLL_MESSAGE
