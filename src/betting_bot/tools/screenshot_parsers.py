import re
from abc import ABC, abstractmethod, ABCMeta

from config import BasketBetKeys
from tools import ocr


class ScreenshotParser(ABCMeta):
    sport: str = NotImplemented
    bookmaker: str = NotImplemented
    categories: list[str] = NotImplemented

    @classmethod
    @abstractmethod
    def to_json(cls, img_url: str, stake_p: float = None, competition: str = None, ba_category: str = None):
        ...


class BasketballParser(ABC):
    sport = "Basketball"

    # TODO(rfo): Get those fields from the BetAnalytix web export
    bet_types = {
        BasketBetKeys.POINTS: "Over/Under points",
        BasketBetKeys.REBONDS: "Over/Under rebonds",
        BasketBetKeys.PASSES: "Over/Under passes",
        BasketBetKeys.PR: "Over/Under PR",
        BasketBetKeys.RP: "Over/Under RP",
        BasketBetKeys.PP: "Over/Under PP",
        BasketBetKeys.PRP: "Over/Under PRP",
        BasketBetKeys.BEST_OF: "Performance du joueur",
        BasketBetKeys.WINNER: "Vainqueur",
        BasketBetKeys.NONE: "Aucun"
    }

    @classmethod
    @abstractmethod
    def get_bet_type(cls, parsed_text: str):
        ...

    @classmethod
    @abstractmethod
    def winner_bet_parser(cls, parsed_text: str) -> dict:
        ...

    @classmethod
    @abstractmethod
    def best_bet_parser(cls, parsed_text: str) -> dict:
        ...

    @classmethod
    @abstractmethod
    def over_under_bet_parser(cls, parsed_text: str) -> dict:
        ...


class BetclicBasketballParser(BasketballParser, ScreenshotParser):
    bookmaker = 'Betclic'

    @classmethod
    def get_bet_type(cls, parsed_text: str):
        if BasketBetKeys.WINNER in parsed_text or BasketBetKeys.RESULT in parsed_text:
            return cls.bet_types.get(BasketBetKeys.WINNER)
        elif BasketBetKeys.BEST_OF in parsed_text:
            return cls.bet_types.get(BasketBetKeys.BEST_OF)
        elif BasketBetKeys.POINTS in parsed_text:
            if BasketBetKeys.REBONDS in parsed_text:
                if BasketBetKeys.PASSES in parsed_text:
                    return cls.bet_types.get(BasketBetKeys.PRP)
                else:
                    return cls.bet_types.get(BasketBetKeys.PR)
            else:
                if BasketBetKeys.PASSES in parsed_text:
                    return cls.bet_types.get(BasketBetKeys.PP)
                else:
                    return cls.bet_types.get(BasketBetKeys.POINTS)
        else:
            if BasketBetKeys.REBONDS in parsed_text:
                if BasketBetKeys.PASSES in parsed_text:
                    return cls.bet_types.get(BasketBetKeys.RP)
                else:
                    return cls.bet_types.get(BasketBetKeys.REBONDS)
            else:
                if BasketBetKeys.PASSES in parsed_text:
                    return cls.bet_types.get(BasketBetKeys.PASSES)
                else:
                    return cls.bet_types.get(BasketBetKeys.NONE)

    @classmethod
    def winner_bet_parser(cls, parsed_text: str) -> dict:
        lines = parsed_text.split('\n')
        bet_data = {
            'match': lines[0],
        }
        if ' - ' in lines[0]:
            # Get Title
            home_team, away_team = bet_data.get('match').split(' - ')
            winner_team = lines[1]
            if winner_team.split(' ')[-1] == home_team.split(' ')[-1]:
                bet_data['title'] = f'{winner_team} gagne contre {away_team}'
            else:
                bet_data['title'] = f'{winner_team} gagne contre {home_team}'
            # Get Stake
            for i, line in enumerate(lines):
                try:
                    bet_data['stake'] = float(line.replace(',', '.'))
                    break
                except ValueError:
                    bet_data['stake'] = -1.
                    continue
            # Get odds
            for line in lines[i + 1:]:
                try:
                    bet_data['odds'] = float(line.replace(',', '.'))
                    break
                except ValueError:
                    bet_data['odds'] = -1.
                    continue
        else:
            # Get Title
            home_team = lines[0]
            away_team = lines[1]
            winner_team = home_team
            if winner_team.split(' ')[-1] == home_team.split(' ')[-1]:
                bet_data['title'] = f'{winner_team} gagne contre {away_team}'
            else:
                bet_data['title'] = f'{winner_team} gagne contre {home_team}'
            # Get Stake
            for i, line in enumerate(lines):
                try:
                    bet_data['stake'] = float(line.replace(',', '.'))
                    break
                except ValueError:
                    bet_data['stake'] = -1.
                    continue
            # Get odds
            for line in lines[i + 1:]:
                try:
                    bet_data['odds'] = float(line.replace(',', '.'))
                    # TODO: possible fail, à améliorer
                    break
                except ValueError:
                    bet_data['odds'] = -1.
                    continue
        return bet_data

    @classmethod
    def over_under_bet_parser(cls, parsed_text: str) -> dict:
        """

        bets_data = {
            "title": ...,
            "stake": ...,
            "odds": ...,
        }
        :param parsed_text:
        :return:
        """
        lines = parsed_text.split('\n')
        bet_data = {}
        # Confirmed bet
        if "Gains possibles" in parsed_text:
            # Find name
            home_team = lines[0]
            away_team = lines[1]
            try:
                mise_line_index = lines.index("Mise")
            except ValueError:
                mise_line_index = -1
            bet_name = f"{lines[mise_line_index - 2]} {lines[mise_line_index - 1]}".split(
                ":"
            )[-1].replace(
                " de ", ""
            )
            while bet_name.startswith(" "):
                bet_name = bet_name[1:]
            bet_data["title"] = f"{bet_name} {cls.get_bet_type(parsed_text).split(' ')[-1]} dans {home_team} - {away_team}"

            # Find stake
            for line in lines:
                if "€" in line:
                    try:
                        stake = float(line.replace(' €', '').replace(',', '.'))
                        if bet_data.get('stake') is None:
                            bet_data['stake'] = stake
                        else:
                            if stake < bet_data.get('stake'):
                                bet_data['stake'] = stake
                    except ValueError:
                        pass
            # Find odd
            for line in lines[::-1]:
                if ',' in line:
                    try:
                        bet_data['odds'] = float(line.replace(',', '.'))
                        break
                    except ValueError:
                        pass
        # Pari à confirmer
        else:
            # Get Stake & Odds
            for i, line in enumerate(lines):
                if line == "€":
                    try:
                        bet_data['stake'] = float(lines[i - 1].replace(",", "."))
                    except ValueError:
                        pass
                elif line == "Gains":
                    try:
                        bet_data['odds'] = float(lines[i - 1].replace(",", "."))
                    except ValueError:
                        pass
            # Get name
            if cls.get_bet_type(parsed_text) == cls.bet_types.get(BasketBetKeys.POINTS):
                player_name = lines[1]
                try:
                    nb_pts = float(re.sub("[^0-9]", "", lines[2])) - 0.5
                    bet_data["title"] = f"{player_name} +{nb_pts} points dans {lines[0]}"
                except ValueError:
                    pass
            else:
                bet_name = lines[1].replace(" de ", "")
                bet_data["title"] = f"{bet_name} {cls.get_bet_type(parsed_text).split(' ')[-1]} dans {lines[0]}"
        return bet_data

    @classmethod
    def best_bet_parser(cls, txt: str) -> dict:
        pass

    @classmethod
    def to_json(cls, img_url: str, stake_p: str = None, competition: str = None, ba_category: str = None):
        parsed_text = ocr.detect_text_uri(img_url)
        data = {
            'bookmaker': cls.bookmaker,
            'sport': cls.sport,
            'bet_type': cls.get_bet_type(parsed_text),
            'stake_p': stake_p,
            'competition': competition,
            'ba_category': ba_category,
        }
        if data['bet_type'] == cls.bet_types.get(BasketBetKeys.WINNER):
            data.update(cls.winner_bet_parser(parsed_text))
        elif data['bet_type'] == cls.bet_types.get(BasketBetKeys.BEST_OF):
            data.update(cls.best_bet_parser(parsed_text))
        # elif data['bet_type'] == cls.bet_types.get(BasketBetKeys.NONE):
        #     pass
        else:
            data.update(cls.over_under_bet_parser(parsed_text))
        return data


class WinamaxBasketballParser(BasketballParser, ScreenshotParser):
    bookmaker = "Winamax"

    @classmethod
    def get_bet_type(cls, parsed_text: str):
        if BasketBetKeys.WINNER in parsed_text or BasketBetKeys.RESULT in parsed_text:
            return cls.bet_types.get(BasketBetKeys.WINNER)
        elif BasketBetKeys.BEST_OF in parsed_text:
            return cls.bet_types.get(BasketBetKeys.BEST_OF)
        elif BasketBetKeys.POINTS in parsed_text:
            if BasketBetKeys.REBONDS in parsed_text:
                if BasketBetKeys.PASSES in parsed_text:
                    return cls.bet_types.get(BasketBetKeys.PRP)
                else:
                    return cls.bet_types.get(BasketBetKeys.PR)
            else:
                if BasketBetKeys.PASSES in parsed_text:
                    return cls.bet_types.get(BasketBetKeys.PP)
                else:
                    return cls.bet_types.get(BasketBetKeys.POINTS)
        else:
            if BasketBetKeys.REBONDS in parsed_text:
                if BasketBetKeys.PASSES in parsed_text:
                    return cls.bet_types.get(BasketBetKeys.RP)
                else:
                    return cls.bet_types.get(BasketBetKeys.REBONDS)
            else:
                if BasketBetKeys.PASSES in parsed_text:
                    return cls.bet_types.get(BasketBetKeys.PASSES)
                else:
                    return cls.bet_types.get(BasketBetKeys.NONE)

    @classmethod
    def winner_bet_parser(cls, parsed_text: str) -> dict:
        pass

    @classmethod
    def best_bet_parser(cls, parsed_text: str) -> dict:
        pass

    @classmethod
    def over_under_bet_parser(cls, parsed_text: str) -> dict:
        """

        bet_data = {
            "title": ...,
            "stake": ...,
            "odds": ...,
        }

        :param parsed_text:
        :return:
        """
        lines = parsed_text.split('\n')
        bet_data = {}
        # Not sended bet
        if "Mise" in lines:
            lines.remove("Mise")
            try:
                lines.remove('F')
            except ValueError:
                pass
            match = lines[0]
            team1 = match.split(' - ')[0].split(' ')[-1]
            team2 = match.split(' ')[-1]
            for i, line in enumerate(lines):
                if "Plus de" in line or "Moins de" in line:
                    player = lines[i - 1].split(' - ')[-1]
                    perf = lines[i].replace("Moins de ", "-").replace("Plus de ", "+").replace(",", ".")

            stake = None
            odd = 0.
            for line in lines:
                if "€" in line:
                    try:
                        euros = float(line.replace(",", ".").replace(" €", ""))
                    except ValueError:
                        break
                    if stake is None:
                        stake = euros
                    elif stake > euros:
                        stake = euros
                if "Cote" in line:
                    try:
                        odd = float(line.replace(",", ".").replace("Cote ", ""))
                    except ValueError:
                        break

            bet_data = {
                "title": f"{player} {perf} {cls.get_bet_type(parsed_text).split(' ')[-1]} dans {match}",
                "stake": stake,
                "odds": odd,
                "teams": [team1, team2]
            }

        # Validated bet
        else:
            if len(lines) == 5:
                odd = lines[0].split(" ")[-1]
                lines[0] = lines[0].replace(f' {odd}', '')

                match_and_date = lines[2].split(" ")
                date = f'{match_and_date[-2]} {match_and_date[-1]}'
                lines[2] = lines[2].replace(f' {date}', '')
                lines.insert(4, odd)
                lines.insert(5, date)
                if lines[2] == lines[5]:
                    lines[2] = lines[1]
                    lines[1] = ""
            elif len(lines) == 6:
                if ':' in lines[2]:
                    match_and_date = lines[2].split(" ")
                    date = f'{match_and_date[-2]} {match_and_date[-1]}'
                    lines[2] = lines[2].replace(f' {date}', '')
                    lines.insert(5, date)
                else:
                    odd = lines[0].split(" ")[-1]
                    lines[0] = lines[0].replace(f' {odd}', '')
                    lines.insert(4, odd)
            if len(lines) == 7:
                try:
                    bet_data['odds'] = float(lines[4].replace(',', '.'))
                except ValueError:
                    bet_data['odds'] = 0.
                try:
                    for line in lines:
                        if "Mise" in line and "€" in line:
                            bet_data['stake'] = float(
                                line.replace(
                                    "Mise ", ""
                                ).replace(
                                    " €", ""
                                ).replace(
                                    ",", "."
                                )
                            )
                except ValueError:
                    bet_data['stake'] = 0.
                bet_cat = cls.get_bet_type(parsed_text).split(' ')[-1]
                player_score = f'{lines[0]} {lines[1]}'.split(" - ")[-1].replace(
                    "Moins de ", "-"
                ).replace(
                    "Plus de ", "+"
                ).replace(
                    ",", "."
                )
                match = lines[2]
                bet_data['title'] = f'{player_score} {bet_cat} dans {match}'.replace(
                    "  ", " "
                )

        return bet_data

    @classmethod
    def to_json(cls, img_url: str, stake_p: str = None, competition: str = None, ba_category: str = None):
        parsed_text = ocr.detect_text_uri(img_url)
        data = {
            'bookmaker': cls.bookmaker,
            'sport': cls.sport,
            'bet_type': cls.get_bet_type(parsed_text),
            'stake_p': stake_p,
            'competition': competition,
            'ba_category': ba_category,
        }
        if data['bet_type'] == cls.bet_types.get(BasketBetKeys.WINNER):
            data.update(cls.winner_bet_parser(parsed_text))
        elif data['bet_type'] == cls.bet_types.get(BasketBetKeys.BEST_OF):
            data.update(cls.best_bet_parser(parsed_text))
        # elif data['bet_type'] == cls.bet_types.get(BasketBetKeys.NONE):
        #     pass
        else:
            data.update(cls.over_under_bet_parser(parsed_text))
        return data
