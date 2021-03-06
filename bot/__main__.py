"""
Initializes the bot

This includes importing the bot, loading the cogs, setting the prefix, etc.
"""

import os
import logging

from discord import Intents

from bot import cogs, google
from bot.bot import Bot

# Create Bot
intents = Intents.default()
intents.members = True
bot = Bot(command_prefix="!" if not os.getenv("DEBUG") else "^", intents=intents)

# Load Cogs
for cog in cogs.names:
    try:
        bot.load_extension("bot.cogs." + cog)
        logging.debug("Loaded cogs.%s", cog)
    except Exception as e:
        logging.warning("Failed to load cogs.%s", cog)
        logging.error(type(e).__name__, e)

# Run Bot
if not (token := os.getenv("TOKEN")):
    logging.error(".env - 'TOKEN' key not found. Cannot start bot.")
    raise EnvironmentError

bot.run(token)
