import asyncio
import os
import random
import time

import discord
import pyttsx3

if __name__ == '__main__':
    intents = discord.Intents.all()
    client = discord.Client(intents=intents)
    token = open('token.txt', 'r').read()

    active_channels = dict()
    things_to_say = ["Posture Check, Bitches",
                    "Posture Check",
                    "Check your fucking posture",
                    "Stretch those backs. It's posture check time."]

    def log_channel_activity(voice_channel):
        if voice_channel.members:
            if voice_channel in active_channels:
                pass
            else:
                active_channels[voice_channel] = time.time()
                print("{}: {}".format(time.ctime(time.time()), voice_channel.id))
        else:
            active_channels.pop(voice_channel, None)

        # print(active_channels)

    # def generate_voice_line():
    #     engine = pyttsx3.init()
    #     list_of_voices = [voice for voice in engine.getProperty('voices')]
    #     chosen_voice = random.choice(list_of_voices)
    #     line_to_say = random.choice(things_to_say)
    #     engine.setProperty('voice', chosen_voice.id)
    #     engine.save_to_file(line_to_say, 'posture_check.mp3')
    #     engine.runAndWait()

    def select_voice_line():
        path = './voice_lines'
        all_mp3 = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.mp3')]
        return random.choice(all_mp3)

    async def active_channel_mapping():
        await client.wait_until_ready()

        while not client.is_closed():
            try:
                for guild in client.guilds:
                    for voice_channel in guild.voice_channels:
                        if voice_channel.name != 'AFK':
                            log_channel_activity(voice_channel)

                await asyncio.sleep(10)
            
            except Exception as e:
                print(str(e))
                await asyncio.sleep(10)

    async def posture_check():
        await client.wait_until_ready()

        while not client.is_closed():
            try:
                for channel in active_channels:
                    if (time.time() - active_channels[channel]) >= (30* 60):
                        print("{}: Entering {} for posture check".format(time.ctime(time.time()), channel.name))
                        v_p = await channel.connect()
                        file = select_voice_line()
                        v_p.play(discord.FFmpegPCMAudio(file))
                        await asyncio.sleep(30)
                        await v_p.disconnect()
                        print("{}: Disconnected from {}".format(time.ctime(time.time()), channel.name))
                        active_channels[channel] = time.time()
                
                await asyncio.sleep(10)
                
            except Exception as e:
                print("{}: {}".format(time.ctime(time.time()), str(e)))
                await asyncio.sleep(10)

    async def join_channel():
        for voice_channel in active_channels:
            await voice_channel.connect()


    @client.event
    async def on_ready():
        print(f'{time.ctime(time.time())}: Logged in as {client.user}')
        for guild in client.guilds:
            print(f'{time.ctime(time.time())}: Logged into {guild.name}')

    @client.event
    async def on_message(message):
        pass
        # print(f'{message.guild.name}: {message.channel}: {message.author}: {message.author.name}: {message.content}')
        #await message.add_reaction(client.get_emoji(370365085576724482))

    
    client.loop.create_task(posture_check())
    client.loop.create_task(active_channel_mapping())
    client.run(token)
