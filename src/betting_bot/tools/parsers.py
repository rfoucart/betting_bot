from datetime import datetime, timedelta

from pandas import DataFrame, read_csv

from config import DISCORD


def csv_to_df(filepath: str, dtype_mapping: dict) -> DataFrame:
    """
    Create a DataFrame from a CSV export from Bet Analytix.

    :param filepath: The filepath to the CSV file.
    :param dtype_mapping: Mapping for columns types.
    :return:
    """
    return read_csv(filepath, dtype=dtype_mapping)


def add_review_date(bets_data: DataFrame) -> DataFrame:
    """
    Compute and add the review date for each bet.
    A review for the day X starts at `day X, 6 A.M.` and ends at `day X+1, 5:59 A.M.`.

    :param bets_data: DataFrame loaded from a CSV export from Bet Analytix.
    :return:
    """

    def get_review_date(date: datetime):
        reference_date = date.replace(hour=6, minute=0)
        if date < reference_date:
            return (reference_date - timedelta(days=1)).strftime("%d/%m/%Y")
        else:
            return reference_date.strftime("%d/%m/%Y")

    bets_data['ReviewDate'] = bets_data.Date.apply(get_review_date)
    return bets_data


def replace_nan_with_empty_string(bets_data: DataFrame) -> DataFrame:
    """
    Replace all NaN values with an empty string.

    :param bets_data: DataFrame loaded from a CSV export from Bet Analytix.
    :return:
    """
    return bets_data.replace(float('nan'), '')


def fix_combined_bets(bets_data: DataFrame) -> DataFrame:
    """
    Fill empty fields in columns `Catégorie` and `Type` with the value of the line above.

    :param bets_data: DataFrame loaded from a CSV export from Bet Analytix.
    :return:
    """
    bets_data.Catégorie.ffill(inplace=True)
    bets_data.Type.ffill(inplace=True)
    return bets_data


def merge_similar_bets(bets_data: DataFrame) -> DataFrame:
    """
    Merge bets from Bet Analytics with the same name, cote and date.
    Sum up the values for columns `Mise`, `Gain`, `Bonus de Gain`, `Commission` and `Bénéfice`.
    Empty values for columns `Bookmaker` and `Commentaire`.
    Keep the value of the lowest index for all others columns.

    :param bets_data: DataFrame loaded from a CSV export from Bet Analytix.
    :return:
    """

    def empty_value(_):
        return ''

    return bets_data.groupby(
        ['Intitulé du pari', 'Cote', 'Date', 'Etat'],
        as_index=False,
        sort=False,
        dropna=False
    ).agg(
        {"Date": "first",
         "Bookmaker": empty_value,
         "Tipster": "first",
         "Sport": "first",
         "Catégorie": "first",
         "Compétition": "first",
         "Type de pari": "first",
         "Pari gratuit": "first",
         "Live": "first",
         "Type": "first",
         "Intitulé du pari": "first",
         "Cote": "first",
         "Mise": "sum",
         "Gain": "sum",
         "Bonus de gain": "sum",
         "Commission": "sum",
         "Bénéfice": "sum",
         "Etat": "first",
         "Closing Odds": "first",
         "Commentaire": "sum"}
    )


def parse_percentages_to_float(bets_data: DataFrame) -> DataFrame:
    def float_percents_from_str(x: str):
        if "%" in x:
            return float(x.replace("%", ""))
        else:
            return -1

    bets_data.Commentaire = bets_data.Commentaire.apply(float_percents_from_str)
    return bets_data


def parse_float_to_percentages(bets_data: DataFrame) -> DataFrame:
    def str_from_float(x: float):
        if x == -1:
            return ""
        else:
            return f"{round(x, 2)}%"
    bets_data.Commentaire = bets_data.Commentaire.apply(str_from_float)
    return bets_data


def overwrite_with_percents(bets_data: DataFrame, bankroll: int) -> DataFrame:
    """
    Overwrite the stake and profit columns with the percentage values from the `Commentaire` column.

    :param bets_data: DataFrame loaded from a CSV export from Bet Analytix.
    :param bankroll: Current bankroll value.
    :return: The modified DataFrame.
    """
    def get_reworked_stake_and_profit_percent(original_stake: str, original_profit: str, percent: str, bk: int, result: str) -> tuple[float, float]:
        try:
            percent = float(percent.replace("%", ""))
        except ValueError:
            try:
                return float(original_stake), round(float(original_profit)/float(original_stake), 2)
            except ValueError:
                return 0., 0.
        if result in ["En attente", "Gagné", "Perdu", "Cashout", "Remboursé"]:
            reworked_stake = round(percent / 100 * bk, 2)
            profit_percent = round(
                percent * float(original_profit)/float(original_stake),
                2
            )
            return reworked_stake, profit_percent

    reworked_stakes = []
    reworked_profits = []
    profit_percentages = []
    for stake, profit, comment, bet_result in zip(
        bets_data.Mise, bets_data.Bénéfice, bets_data.Commentaire, bets_data.Etat
    ):
        reworked_stake, profit_percent = get_reworked_stake_and_profit_percent(stake, profit, comment, bankroll, bet_result)
        reworked_stakes.append(reworked_stake)
        reworked_profits.append(profit_percent * bankroll / 100)
        profit_percentages.append(profit_percent)
    bets_data["reworked_stakes"] = reworked_stakes
    bets_data["reworked_profits"] = reworked_profits
    bets_data["profit_percentages"] = profit_percentages

    return bets_data
