""" cog."""

import discord
from discord.ext import commands, tasks

from radia import utils, google


class Roles(commands.Cog):
    """Utility commands for handling roles."""

    def __init__(self, bot):
        self.bot = bot

    @commands.has_role("Staff")
    @commands.group()
    async def bracket(self, ctx):
        """Group of commands handling the bracket roles."""

    @bracket.command()
    async def remove(self, ctx):
        """Remove the bracket roles from members who currently have it."""
        with ctx.typing():
            # Create list of applicable champion roles
            roles = utils.roles.get(ctx,
                "Alpha",
                "Beta",
                "Gamma"
            )
            # Create a set of all members with any bracket role
            all_champions = set()
            for role in roles:
                all_champions.update(role.members)
            # Remove bracket roles from each of those members
            for member in all_champions:
                await member.remove_roles(*roles)

        # Log all members the bracket roles were removed from
        embed = utils.Embed(
            title="Removed bracket roles from:",
            description=utils.Embed.list(f"`{len(all_champions)}` total members."))
        await ctx.send(embed=embed)

    @commands.has_role("Staff")
    @commands.group()
    async def champion(self, ctx):
        """Group of commands handling the champion roles."""
    
    @champion.command(aliases=["coronate", "crown"])
    async def add(self, ctx):
        """Add the Champion role to members."""
        with ctx.typing():
            # Create list of applicable champion roles
            roles = utils.roles.get(ctx,
                "Past Low Ink Winner",
                "Low Ink Current Champions"
            )
            # Add champion roles from every member mentioned
            for member in ctx.message.mentions:
                await member.add_roles(*roles)

        # Log all members the champion roles were added to
        embed = utils.Embed(
            title="Added champion roles to:",
            description=utils.Embed.list(
                [member.mention for member in ctx.message.mentions]))
        await ctx.send(embed=embed)

    @champion.command(aliases=["dethrone"])
    async def remove(self, ctx):
        """Remove the champion roles from members who currently have it."""
        with ctx.typing():
            # Create list of applicable champion roles
            roles = utils.roles.get(ctx,
                "Low Ink Current Champions",
                "Beta Bracket Champions",
                "Gamma Bracket Champions"
            )
            # Create a set of all members with any champion role
            all_champions = set()
            for role in roles:
                all_champions += role.members
            # Remove champion roles from each of those members
            for member in all_champions:
                await member.remove_roles(*roles)

        # Log all members the champion roles were removed from
        embed = utils.Embed(
            title="Removed champion roles from:",
            description=utils.Embed.list(
                [member.mention for member in all_champions]))
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Roles(bot))