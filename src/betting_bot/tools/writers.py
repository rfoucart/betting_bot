from pandas import DataFrame

from config import EMOJI
from messages import NEGATIVE_BANKROLL_MESSAGE


def pending_bets_evaluation(pending_bets: DataFrame, bankroll: int, current_profit: float) -> str:
    """
    Write the review for pending bets, including the range of profit values.

    :param pending_bets: Bets not yet completed (`Etat` == `"En Attente"`).
    :param bankroll: Current bankroll value.
    :param current_profit: Current profit from completed bets for the day.
    :return:
    """
    if bankroll <= 0:
        return NEGATIVE_BANKROLL_MESSAGE
    bk_committed = round(pending_bets.reworked_stakes.sum() / bankroll * 100, 2)
    max_earnings = round(
        (pending_bets.reworked_stakes * (pending_bets.Cote.replace('', 1) - 1)).sum() / bankroll * 100, 2)
    min_evol = round(current_profit - bk_committed, 2)
    max_evol = round(current_profit + max_earnings, 2)
    return (f'Résultat final compris entre {"+" if min_evol >= 0 else ""}{min_evol}% et {"+" if max_evol >= 0 else ""}'
            f'{max_evol}% ({len(pending_bets)} pari{"s" if len(pending_bets) > 1 else ""} encore en cours)')


def simple_bet_line(sport, odd, stake_percentage, bet_result, profit_percentage, bet_name) -> str:
    """
    Write a line for a simple bet.

    :param sport: Sport name.
    :param odd: Odd value.
    :param stake_percentage: Stake percentage.
    :param bet_result: Bet result.
    :param profit_percentage: Profit percentage.
    :param bet_name: Bet name.
    :return: The line for the bet.
    """
    return (f'{sport} |__{odd}__| • {stake_percentage} {bet_result} **(__{"+" if profit_percentage >= 0 else ""}'
            f'{profit_percentage}%__)** {bet_name}')


def winners_count(bets_data: DataFrame) -> str:
    """
    Write the count of winning bets.

    :param bets_data: Dataframe containing the bets.
    :return: The count of winning bets.
    """
    return f'\n:scales: **Paris gagnants : {len(bets_data[bets_data["Etat"] == "Gagné"])}/{len(bets_data)} :ticket:**'


def review_last_lines(bets_data: DataFrame, bankroll: int) -> list[str]:
    """
    Write the final review lines.

    :param bets_data: Dataframe containing the bets.
    :param bankroll: Current bankroll value.
    :return: The last lines of the daily review.
    """
    message_lines = []
    bk_result = round(bets_data.reworked_profits.sum() / bankroll * 100, 2)
    pending_bets = bets_data[bets_data.Etat == "En attente"]
    if len(bets_data) > 0:
        message_lines.append(f'**__Résultat {"final" if len(pending_bets) == 0 else "temporaire"} :__ '
                             f'{"+" if bk_result >= 0 else ""}{round(bk_result, 2)}%** '
                             f'{EMOJI.POSITIVE_BALANCE if bk_result >= 0 else EMOJI.NEGATIVE_BALANCE}')
    if len(pending_bets) > 0:
        message_lines.append(pending_bets_evaluation(pending_bets, bankroll, bk_result))
    return message_lines


def review_date_line(date: str) -> str:
    """
    Write the date line for the review.

    :param date: Date of the review.
    :return: The date line.
    """
    return f'\n**__Résultats du {date}__**'
