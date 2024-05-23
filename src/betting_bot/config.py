import os
from enum import StrEnum

from dotenv import load_dotenv

load_dotenv()

EPYBOT_TOKEN = os.getenv("EPYBOT_TOKEN")
COMMAND_PREFIX = os.getenv("COMMAND_PREFIX")
api_sports_key = os.getenv("API_SPORTS_KEY")
DATE_FORMAT = "%d/%m/%Y"


# TODO(rfo) : Gather data from the webapp link instead of keeping them in a file
class FILEPATHS:
    DATA_FOLDER = "../data"
    BA_EXTRACT = os.path.join(DATA_FOLDER, 'Export Bet-Analytix.csv')


class DISCORD:
    MAX_CHARACTERS_LIMIT = 2000
    OWNER_ID = int(os.getenv("OWNER_ID"))
    OWNER_MENTION_ID = f'<@{OWNER_ID}>'
    BOT_KNOWN_BOOKMAKERS = [
        "Betclic",
        "Winamax"
    ]
    # Leave empty to allow all users
    ALLOWED_USERS_IDS = [
        OWNER_ID
    ]
    # Leave empty to allow all channels
    ALLOWED_CHANNEL_IDS = [

    ]


class BET_STATUS:
    LOST = "Perdu"
    WON = "Gagné"
    REFUND = "Remboursé"
    CANCELED = "Annulé"
    PENDING = "En attente"
    CASHOUT = "Cashout"


class EMOJI:
    LOST_BET = ":x:"
    WON_BET = ":white_check_mark:"
    CANCELED_BET = ":recycle:"
    PENDING_BET = ":hourglass:"
    CASHOUT_BET = ":regional_indicator_c: :regional_indicator_o:"
    POSITIVE_BALANCE = ":chart_with_upwards_trend:"
    NEGATIVE_BALANCE = ":chart_with_downwards_trend:"
    SPORTS = {
        "Football": ":soccer:",
        "Tennis": ":tennis:",
        "Volleyball": ":volleyball:",
        "Basketball": ":basketball:",
        "Badminton": ":badminton:",
        "Baseball": ":baseball:",
        "Rugby": ":rugby_football:",
        "Football US": ":football:",
        "Athletisme": ":stadium:",
        "Formule 1": ":racing_car:",
        "Auto-Moto": ":motorcycle:",
        "Tennis de table": ":ping_pong:",
        "Boxe": ":boxing_glove:",
        "MMA": ":boxing_glove:",
        "Cyclisme": ":person_biking:",
        "Handball": ":handball:",
        "Hockey sur glace": ":hockey:",
        "Golf": ":golf:",
        "Snooker": ":8ball:",
        "Flêchettes": ":dart:",
        "Biathlon": ":snowflake:",
        "Ski Alpin": ":skier:",
        "Ski de fond": ":skier:",
        "Autre sport": ":question:"
    }
    FROM_STATUS = {
        BET_STATUS.LOST: LOST_BET,
        BET_STATUS.WON: WON_BET,
        BET_STATUS.REFUND: CANCELED_BET,
        BET_STATUS.CANCELED: CANCELED_BET,
        BET_STATUS.PENDING: PENDING_BET,
        BET_STATUS.CASHOUT: CASHOUT_BET
    }


class BA_EXPORT:
    DTYPE_MAPPING = {
        "Date": object,
        "Bookmaker": str,
        "Tipster": str,
        "Sport": str,
        "Catégorie": str,
        "Compétition": str,
        "Type de pari": str,
        "Pari gratuit": str,
        "Live": str,
        "Type": str,
        "Intitulé du pari": str,
        "Cote": float,
        "Mise": float,
        "Gain": float,
        "Bonus de gain": object,
        "Commission": object,
        "Bénéfice": float,
        "Etat": str,
        "Closing Odds": object,
        "Commentaire": str
    }


class BasketBetKeys(StrEnum):
    POINTS = "points"
    REBONDS = "rebonds"
    PASSES = "passes"
    PR = "PR"
    RP = "RP"
    PP = "PP"
    PRP = "PRP"
    BEST_OF = "Meilleur"
    WINNER = "Vainqueur"
    RESULT = "Résultat"
    NONE = "Aucun"
