import discord
import asyncio
import datetime

if __name__ == '__main__':
    intents = discord.Intents.all()
    client = discord.Client(intents=intents)
    token = open('token.txt', 'r').read()

    active_channels = dict()

    def log_channel_activity(voice_channel):
        if voice_channel.members:
            if voice_channel.id in active_channels:
                pass
            else:
                active_channels[voice_channel.id] = datetime.datetime.now()
                print(voice_channel.id)
        else:
            active_channels.pop(voice_channel, None)

        # print(active_channels)

    async def active_channel_mapping():
        await client.wait_until_ready()

        while not client.is_closed():
            try:
                for guild in client.guilds:
                    for voice_channel in guild.voice_channels:
                        if voice_channel.name != 'AFK':
                            log_channel_activity(voice_channel)

                await asyncio.sleep(60)
            
            except Exception as e:
                print(str(e))
                await asyncio.sleep(60)

    async def posture_check():
        await client.wait_until_ready()

        while not client.is_closed():
            try:
                for channel in active_channels:
                    if (active_channels[channel] - datetime.datetime.now()).seconds >= 30:
                        # join channel
                        # await channel.connect()?
                        # say posture check
                        # leave channel
                        active_channels[channel] = datetime.datetime.now()
                
                await asyncio.sleep(60)
                
            except Exception as e:
                print(str(e))
                await asyncio.sleep(60)

    def join_channel():
        pass


    @client.event
    async def on_ready():
        print(f'Logged in as {client.user}')
        for guild in client.guilds:
            print(f'Logged into {guild.name}')

    @client.event
    async def on_message(message):
        pass
        # print(f'{message.guild.name}: {message.channel}: {message.author}: {message.author.name}: {message.content}')
        #await message.add_reaction(client.get_emoji(370365085576724482))

    
    client.loop.create_task(posture_check())
    client.loop.create_task(active_channel_mapping())

    client.run(token)