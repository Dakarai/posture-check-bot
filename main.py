import discord
import asyncio
import time

if __name__ == '__main__':
    intents = discord.Intents.all()
    client = discord.Client(intents=intents)
    token = open('token.txt', 'r').read()

    active_channels = dict()

    async def active_channel_mapping():
        await client.wait_until_ready()

        while not client.is_closed():
            try:
                for guild in client.guilds:
                    for voice_channel in guild.voice_channels:
                        if voice_channel.name != 'AFK':
                            print(voice_channel.name)

                await asyncio.sleep(10)
            
            except Exception as e:
                print(str(e))
                await asyncio.sleep(10)



    @client.event
    async def on_ready():
        print(f'Logged in as {client.user}')
        for guild in client.guilds:
            print(f'Logged into {guild.name}')

    @client.event
    async def on_message(message):
        print(f'{message.guild.name}: {message.channel}: {message.author}: {message.author.name}: {message.content}')
        #await message.add_reaction(client.get_emoji(370365085576724482))

    client.loop.create_task(active_channel_mapping())
    client.run(token)
    