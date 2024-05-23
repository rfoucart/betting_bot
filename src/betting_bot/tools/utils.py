from datetime import datetime, timedelta


def get_date_bounds(date: str, n_days=1):
    """
    Compute datetimes for the `date` with duration `n_days`.
    `start_date` starts at 6 A.M. for the `date` provided.
    `end_date` is `start_date` + `n_days`.

    :param date: String representing the date, in format "DDMMYY", where DD is the day, MM is the month and YY is the
    year.
    :param n_days: :return:
    """
    if n_days < 0:
        raise ValueError("Number of days must be a non-negative integer.")
    start_date = datetime.strptime(date, "%d%m%y") + timedelta(hours=6)
    end_date = start_date + timedelta(days=n_days)
    return start_date, end_date


def list_to_str(strings: list[str], sep='\n') -> str:
    """
    Converts a list of strings into a single string.

    This function takes a list of strings and concatenates them into a single string.
    Each string in the list is separated by the specified separator, which is a newline character by default.

    :param strings: A list of strings to be concatenated.
    :param sep: The separator to be used between each string. Default is a newline character.
    :return: A single string made up of all the strings in the list, separated by the specified separator.
    """
    return sep.join(strings)
