import traceback

import discord.ext.commands
from discord import app_commands
from discord.app_commands import Range
from discord.ext import commands

import sports_api.classes
from config import EPYBOT_TOKEN, DISCORD, FILEPATHS, COMMAND_PREFIX
from messages import UNALLOWED_USER_MESSAGE, UNALLOWED_CHANNEL_MESSAGE, REVIEW_SIGNATURE_MESSAGE
from tools.post_generators import ba_generic_review
from tools.utils import list_to_str

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)


@bot.tree.command()
@app_commands.describe(
    date="Date of the review (format : DDMMYY)",
    bankroll="(Optionnal) The current bankroll value"
)
async def get_review(interaction: discord.Interaction, date: Range[str, 6, 6], bankroll: str = "2000"):
    if DISCORD.ALLOWED_USERS_IDS and interaction.user.id not in DISCORD.ALLOWED_USERS_IDS:
        await interaction.response.send_message(UNALLOWED_USER_MESSAGE + f"{DISCORD.ALLOWED_USERS_IDS}", ephemeral=True)
        return
    if DISCORD.ALLOWED_CHANNEL_IDS and interaction.channel.id not in DISCORD.ALLOWED_CHANNEL_IDS:
        await interaction.response.send_message(UNALLOWED_CHANNEL_MESSAGE, ephemeral=True)
        return
    discord_posts = [f"## :bar_chart: Résultats du __{date[0:2]}/{date[2:4]}/{date[4:6]}__ :"]
    try:
        post = ba_generic_review(review_file=FILEPATHS.BA_EXTRACT,
                                 date=date,
                                 bankroll=int(bankroll))
        discord_posts.append(post)
    except Exception as e:
        traceback.print_exception(e)
        discord_posts.append(f'```accesslog\n{list_to_str(traceback.format_exception(e)[-2:])}```')

    discord_posts.append(REVIEW_SIGNATURE_MESSAGE)

    await interaction.response.defer()
    webhook = interaction.followup
    discord_posts = list_to_str(discord_posts)
    while len(discord_posts) > DISCORD.MAX_CHARACTERS_LIMIT:
        cut_index = discord_posts.rfind("\n", 0, DISCORD.MAX_CHARACTERS_LIMIT) + 1
        part1, discord_posts = discord_posts[:cut_index], discord_posts[cut_index:]
        await webhook.send(part1)
    await webhook.send(discord_posts)


@bot.tree.command()
@app_commands.describe(
    date="format: DDMMYY"
)
async def get_nba_matches(interaction, date: Range[str, 6, 6]):
    if interaction.user.id not in DISCORD.ALLOWED_USERS_IDS:
        return
    formatted_date = f'20{date[4:6]}-{date[2:4]}-{date[0:2]}'
    daily_match_data = sports_api.classes.BasketballAPI.get_nba_match_dates(formatted_date)
    if interaction.user.id == DISCORD.OWNER_ID:
        sports_api.classes.BasketballAPI.write_data(daily_match_data)
    matches_summary = []
    last_minute = -2
    i = 1
    for match in daily_match_data:
        if int(match.get('minute')) == (last_minute + i):
            match['minute'] = str(last_minute).zfill(2)
            i += 1
        else:
            matches_summary.append('')
            i = 1
        last_minute = int(match.get('minute'))
        matches_summary.append(f'[{match.get("day")} {match.get("month")} {match.get("year")} {match.get("hour")}:'
                               f'{match.get("minute")}] {match.get("name")}')
    await interaction.response.send_message(
        f"Found {len(daily_match_data)} matches :\n```accesslog\n{list_to_str(matches_summary)}\n```",
        ephemeral=True
    )


@bot.command()
async def sync(ctx):
    """
    This is a command for the bot that synchronizes the bot's commands with the Discord server.

    This command is only accessible by the owner of the bot. If the command is invoked by the owner, it will sync the
    bot's commands with all the Discord servers the bot has joined and send a message with the synced commands. If the
    command is invoked by any other user, it will send a message indicating that the user is not allowed to use this
    command.

    :param ctx: The context in which the command was called. This contains information about the message,
    the channel, and the server.
    :return: None
    """
    if ctx.message.author.mention == DISCORD.OWNER_MENTION_ID:
        commands_synced = await bot.tree.sync(guild=None)
        sep_commands = "\n* "
        commands_synced_message = \
            (f"Synced commands with all servers.\n\n"
             f"__Commands synced :__\n"
             f"* {sep_commands.join([f'**{command.name}** with id={command.id}' for command in commands_synced])}"
             f"You should wait a few minutes for the changes to apply.")

        await ctx.send(commands_synced_message)
    else:
        await ctx.send(UNALLOWED_USER_MESSAGE)


if __name__ == "__main__":
    bot.run(EPYBOT_TOKEN)
