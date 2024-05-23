from config import DISCORD

UNALLOWED_USER_MESSAGE = (f"Tu ne fais pas partie des utilisateurs autorisés à me consulter.\nSi tu veux te plaindre, "
                          f"contacte mon créateur {DISCORD.OWNER_MENTION_ID}")
UNALLOWED_CHANNEL_MESSAGE = ("Je ne suis pas autorisé à répondre dans ce canal de discussion.\nContacter {"
                             "DISCORD.OWNER_MENTION_ID} pour toute modification.")

REVIEW_SIGNATURE_MESSAGE = f'*Pour toute remarque sur le bilan, mentionnez {DISCORD.OWNER_MENTION_ID} :saluting_face:*'

NO_BET_MESSAGE = f"Aucun pari n'a été trouvé pour cette journée.\n\n"

NEGATIVE_BANKROLL_MESSAGE = "Bankroll non positive, impossible de calculer le résultat final."
