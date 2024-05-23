from datetime import datetime

from pandas import DataFrame, to_datetime


def filter_by_category(bets_data: DataFrame, category: str) -> DataFrame:
    """
    Return a dataframe containing lines with the matching category.

    :param bets_data: Dataframe generated from a BetAnalytix export.
    :param category: Either 'boosts' or 'values'
    :return: The filtered dataframe with the matching category
    """
    return bets_data[bets_data.Catégorie.isin([category])]


def filter_by_date(bets_data: DataFrame, start_date: datetime.date, end_date: datetime.date, sort: bool) -> DataFrame:
    """
    This function removes entries outside the range of [start_date, end_date] and returns the resulting sub-dataframe.

    :param bets_data: DataFrame loaded from a CSV export from Bet Analytix.
    :param start_date: All bets before this date are removed.
    :param end_date: All bets after this date are removed.
    :param sort: If True, sort the bets in the final dataframe by date.
    :return:
    """
    bets_data.Date = to_datetime(bets_data["Date"], format="%d/%m/%Y %H:%M")
    final_data_frame = bets_data[(bets_data.Date >= start_date) & (bets_data.Date < end_date)]
    if sort:
        final_data_frame = final_data_frame.sort_values(by=["Date"])
    return final_data_frame
