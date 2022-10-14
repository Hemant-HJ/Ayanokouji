import os
import aiohttp
import discord
from discord.ext import commands

import config

def get_prefix():
    pass

class Ayanokouji(commands.Bot):
    def __init__(self):
        self.error_message = []
        super().__init__(
            command_prefix = commands.when_mentioned_or(
                'ayanokouji',
                'aya'
            ),
            intents = discord.Internts.all(),
            stripe_after_prefix = True,
            self_bot = False,
            allowed_mention = discord.AllowedMentions(everyone = False, users = True, roles = False, replied_user = True)
        )

    async def on_ready(self):
        print(f'Bot Logged in {self.user.name} {self.user.id}')

    async def setup_hook(self):
        for cog in self.cogs:
            try:
                await self.load_extension(cog)
            except:
                self.error_message.append(cog.title())
        
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(config.WEBHOOK, session = session)
            e = discord.Embed(
                title = f'Hi {self.owner.name}',
                description = 'Loaded all cogs.',
                color = discord.Color.blue(),
                timestamp = discord.utils.utcnow()
            )
            if self.error_message:
                e.description = 'Loaded all cogs except:'
                e.add_field(
                    name = 'Unloaded Cogs',
                    value = '\n'.join(self.error_message),
                    inline = False
                )
            await webhook.send(embed = e, username = 'Ayanokouji', content = 'Bot Online.')

    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content == f'<{self.user.id}>':
            e = discord.Embed(
                title = 'Ayanokouji',
                description = 'Just a normal bot trying to help my owner.',
                color = discord.Color.blue(),
                timestamp = discord.utils.utcnow()
            )
        self.process_commands(message)