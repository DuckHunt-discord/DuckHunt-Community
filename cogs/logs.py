# -*- coding: utf-8 -*-
# !/usr/bin/env python3.5

"""

"""
import datetime
import json
import logging

import discord


class Logs:


    def __init__(self, bot):
        self.bot = bot
        self.channel = "297750761365045249"
        self.root_dir = self.bot.where + "/users/"
        self.logger = logging.getLogger('cbot')


    async def get_and_assign_roles(self, member):
        try:
            file_name = str(member.id) + ".json"
            with open(self.root_dir + file_name, "r") as infile:
                m_roles = json.load(infile)
        except FileNotFoundError:
            return []

        roles = []


        for role in member.server.roles:
            if role.id in m_roles:
                roles.append(role)
        roles_names = [r.name for r in roles]


        self.logger.info(f"Adding role(s) {roles_names} to {member.name}, as requested by get_and_assign_roles in the file {self.root_dir}{file_name}")
        await self.bot.add_roles(member, *roles)

        return [r.name for r in roles]

    async def save_roles(self, member):
        file_name = str(member.id) + ".json"
        roles = member.roles
        roles_ids = [r.id for r in roles].remove("322707763992199170") #Sans @everyone
        with open(self.root_dir + file_name, "w") as outfile:
            json.dump(roles_ids, outfile)
        return [r.name for r in roles]



    async def on_member_join(self, member):
        roles_name = await self.get_and_assign_roles(member)

        channel = self.bot.get_channel(self.channel)
        embed = discord.Embed()
        embed.colour = discord.Colour.green()
        embed.title = "User {u} joined".format(u=member.name + "#" + member.discriminator)
        embed.timestamp = datetime.datetime.now()
        embed.set_author(name=member.id, icon_url=member.avatar_url)
        embed.description = f"Restored roles : {roles_name}"
        await self.bot.send_message(channel, embed=embed)

    async def on_member_remove(self, member):
        roles_name = await self.save_roles(member)
        channel = self.bot.get_channel(self.channel)

        embed = discord.Embed()
        embed.colour = discord.Colour.red()
        embed.title = "User {u} left".format(u=member.name + "#" + member.discriminator)
        embed.timestamp = datetime.datetime.now()
        embed.set_author(name=member.id, icon_url=member.avatar_url)
        embed.description = f"Saved roles : {roles_name}"
        await self.bot.send_message(channel, embed=embed)


def setup(bot):
    bot.add_cog(Logs(bot))
