class BetOdds:
    """
    A class used to represent the odds of a bet.

    :ivar _odds: a tuple representing the odds of the bet
    :ivar _n_odds: the number of odds
    :ivar _margin: the margin of the bet
    :ivar _odds_without_margin: a tuple representing the odds of the bet without the margin
    :ivar _true_probs: a tuple representing the true probabilities of the odds
    """

    def __init__(self, odds: tuple):
        """
        Constructs all the necessary attributes for the BetOdds object.

        :param odds: a tuple representing the odds of the bet
        """
        self._odds = odds
        self._n_odds = len(odds)
        self._margin = None
        self._odds_without_margin = None
        self._true_probs = None

        self.compute_margin()
        self.compute_true_odds()

    def compute_true_odds(self):
        """
        Computes the true odds of the bet.
        """
        true_odds = []
        for odd in self._odds:
            true_odds.append(
                (self._n_odds * odd) / (self._n_odds - self._margin * odd)
            )
        self._odds_without_margin = tuple(true_odds)
        self._true_probs = tuple(1 / odd for odd in true_odds)

    def compute_margin(self):
        """
        Computes the margin of the bet.
        """
        prob_sum = 0
        for odd in self._odds:
            prob_sum += 1/odd
        self._margin = 1 - 1/prob_sum

    @property
    def odds(self):
        """
        Returns the odds of the bet.
        """
        return self._odds

    @odds.setter
    def odds(self, new_odds):
        """
        Sets the odds of the bet.

        :param new_odds: a tuple representing the new odds of the bet
        """
        if type(new_odds) != tuple:
            raise TypeError("Odds must be a tuple.")
        if any(odd < 1 for odd in new_odds):
            raise ValueError("Odds value cannot be less than 1.")
        self._odds = new_odds

    @property
    def odds_without_margin(self):
        """
        Returns the fair odds of the bet.
        """
        return self._odds_without_margin

    @property
    def true_probs(self):
        """
        Returns the fair probabilities of the bet.
        """
        return self._true_probs

    @property
    def margin(self):
        """
        Returns the margin of the bet.
        """
        return self._margin
