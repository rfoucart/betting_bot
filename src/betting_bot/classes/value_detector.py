import pandas as pd
from pandas import DataFrame

from classes.bet_odds import BetOdds


class ValueDetector:
    """
    A class used to detect the value in betting odds.

    :ivar _values: a tuple holding the computed values
    :ivar _kelly: a tuple holding the computed Kelly criterion values
    :ivar _stakes: a tuple holding the computed estimated stakes
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the ValueDetector object.
        """
        self._values = None
        self._kelly = None
        self._stakes = None

    def _compute_values(self, ref_odds: BetOdds, book_odds: BetOdds):
        """
        Computes the values based on the reference and bookmaker odds.

        :param ref_odds: The reference odds.
        :type ref_odds: BetOdds
        :param book_odds: The bookmaker odds.
        :type book_odds: BetOdds
        """
        self._values = tuple(prob * odd - 1 for prob, odd in zip(ref_odds.true_probs, book_odds.odds))

    def _compute_kelly_criterion(self, book_odds: BetOdds):
        """
        Computes the Kelly criterion based on the bookmaker odds.

        :param book_odds: The bookmaker odds.
        :type book_odds: BetOdds
        """
        self._kelly = tuple(value / (odd - 1) for value, odd in zip(self._values, book_odds.odds))

    def _compute_estimated_stake(self, book_odds: BetOdds):
        """
        Computes the estimated stakes based on the bookmaker odds.

        :param book_odds: The bookmaker odds.
        :type book_odds: BetOdds
        """
        self._stakes = tuple(kelly / odd for kelly, odd in zip(self._kelly, book_odds.odds))

    def analyze(self, ref_odds: BetOdds, book_odds: BetOdds, bet_names: tuple[str, ...]) -> DataFrame:
        """
        Analyzes the betting odds and returns a DataFrame with the results.

        :param ref_odds: The reference odds.
        :type ref_odds: BetOdds
        :param book_odds: The bookmaker odds.
        :type book_odds: BetOdds
        :param bet_names: The names of the bets.
        :type bet_names: tuple[str]
        :return: A DataFrame with the results of the analysis.
        :rtype: DataFrame
        """
        self._compute_values(ref_odds, book_odds)
        self._compute_kelly_criterion(book_odds)
        self._compute_estimated_stake(book_odds)

        return pd.DataFrame(
            {
                "Result": bet_names,
                "FR_Odds": book_odds.odds,
                "ps3838": ref_odds.odds,
                "True_Odds": ref_odds.odds_without_margin,
                "Probs": ref_odds.true_probs,
                "Values": self._values,
                "Kelly": self._kelly,
                "Stakes": self._stakes
            }
        )

    @staticmethod
    def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        """
        Cleans the DataFrame and returns it.

        :param df: The DataFrame to be cleaned.
        :type df: DataFrame
        :return: The cleaned DataFrame.
        :rtype: DataFrame
        """
        def convert_float_to_percentage(x):
            return f"{round(x * 100, 2)}%"

        def round_odds(x):
            return round(x, 2)
        df.Probs = df.Probs.apply(convert_float_to_percentage)
        df.Values = df.Values.apply(convert_float_to_percentage)
        df.Kelly = df.Kelly.apply(convert_float_to_percentage)
        df.Stakes = df.Stakes.apply(convert_float_to_percentage)
        df.True_Odds = df.True_Odds.apply(round_odds)

        return df
