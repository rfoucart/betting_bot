from config import EMOJI, BA_EXPORT
from messages import NO_BET_MESSAGE
from tools.filters import filter_by_date
from tools.parsers import csv_to_df, add_review_date, replace_nan_with_empty_string, fix_combined_bets, \
    merge_similar_bets, overwrite_with_percents, parse_percentages_to_float, parse_float_to_percentages
from tools.utils import get_date_bounds, list_to_str
from tools.writers import simple_bet_line, winners_count, review_last_lines, review_date_line


def ba_generic_review(review_file: str, date: str, bankroll: int) -> str:
    """
    Generates the Discord's message review from BetAnalytix export file.

    :param review_file: The path to the CSV export from BetAnalytix.
    :param date: The starting date for the review, in format `DDMMYY`.
    :param bankroll: The current bankroll.
    :return:
    """
    message_lines = []

    # Preprocessing the data from BetAnalytix
    all_bets = (
        parse_float_to_percentages(
            merge_similar_bets(
                parse_percentages_to_float(
                    replace_nan_with_empty_string(
                        fix_combined_bets(
                            csv_to_df(
                                review_file,
                                BA_EXPORT.DTYPE_MAPPING
                            )
                        )
                    )
                )
            )
        )
    )

    # Filtering the data by date
    start_date, end_date = get_date_bounds(date, n_days=1)
    bets_data = (
            add_review_date(
                filter_by_date(
                    bets_data=all_bets,
                    start_date=start_date,
                    end_date=end_date,
                    sort=True
                )
            )
    )
    bets_data = overwrite_with_percents(bets_data, bankroll)
    review_dates = bets_data.ReviewDate.unique()
    if len(review_dates) == 0:
        message_lines.append(NO_BET_MESSAGE)
    else:
        review_date = review_dates[0]
        message_lines.append(review_date_line(review_date))
        for bet in bets_data[bets_data.ReviewDate == review_date].itertuples():
            if bet.Type == "Simple":  # Ignore other types of bets
                if "%" in bet.Commentaire:
                    stake_percentage = bet.Commentaire
                    profit_percentage = bet.profit_percentages
                else:
                    stake_percentage = round((bet.reworked_stakes / bankroll) * 100, 2)
                    profit_percentage = round(bet.profit_percentages * (bet.reworked_stakes / bankroll) * 100, 2)

                message_lines.append(
                    simple_bet_line(
                        sport=EMOJI.SPORTS[bet.Sport],
                        odd=bet.Cote,
                        stake_percentage=stake_percentage,
                        bet_result=EMOJI.FROM_STATUS[bet.Etat],
                        profit_percentage=profit_percentage,
                        bet_name=bet[11]
                    )
                )
    message_lines.append(winners_count(bets_data))
    message_lines.extend(review_last_lines(bets_data, bankroll))
    return list_to_str(message_lines)
