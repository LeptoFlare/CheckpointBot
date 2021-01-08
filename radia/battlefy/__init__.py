"""Initializes the Battlefy connector."""

import logging
import aiohttp

from .objects import Player, Team, Tournament


class Connector:
    """Battlefy connector."""

    def __init__(self):
        self.session = aiohttp.ClientSession()
        logging.debug("Loaded battlefy.connector")

    async def query(self, url):
        """Get a response at url."""
        async with self.session.get("https://dtmwra1jsgyb0.cloudfront.net/" + url) as response:
            if response.status != 200:
                logging.error("Unable to query battlefy api, Status Code: %s", response.status)
                return
            return await response.json()

    async def get_tournament(self, tournament):
        """ Get tournament object from battlefy api.

        :param tournament str: Battlefy Tournament ID
        :return Tournament: A Tournament object
        """
        battlefy_tournament = await self.query(f"tournaments/{tournament}")
        battlefy_teams = await self.query(f"tournaments/{tournament}/teams")
        return Tournament(battlefy_tournament, battlefy_teams)

    async def get_teams(self, *args):
        """Helper function that simply returns the ".teams" attribute of a tournament."""
        tourney = await self.get_tournament(*args)
        return tourney.teams

connector = Connector()
