# bot.py
import os
import random
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

tree = {
    "So I only talk to people who know my street name. What's my name?": ([], [
            {"userRes": "the great one", "after":[], "nextQuestion": "Chunky or smooth?"}, 
            {"userRes":"", "after": ["Hmmm explore the puzzles and come back when u know it"]}
        ]),
    "Chunky or smooth?": (["To receive the password, you must answer one question correctly."], 
        [
            {"userRes": "smooth", "after":["Yes, smooth like my belly. The password is...frogalicious"]}, 
            {"userRes": "", "after":["U didn\'t choose smooth? Thats mad sus man.", "Get out before Cthulu gets mad"]}
        ]),     
}

 
async def dm_converse(user, tree, question):
    async def send_messages(messages, channel):
        for msg in messages:
            async with channel.typing():
                await channel.send(msg)
                await asyncio.sleep(1)
            
    def check(m):
        return m.channel == user.dm_channel

    setup = tree[question][0]
    responses = tree[question][1]
    await send_messages(setup, user)
    await user.send(question)
    try:
        msg = await bot.wait_for('message', timeout=40.0, check=check)
    except asyncio.TimeoutError:
        await message.author.send('U take too long. Cthulu doesnt get ghosted, Cthulu does the ghosting!')
    else:
        if msg.author == bot.user:
            return
        for response in responses:
            if response["userRes"] in msg.content.lower():
                await send_messages(response["after"], user)
                if "nextQuestion" in response:
                    await dm_converse(user, tree, response["nextQuestion"])
                return
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == "O great Cthulhu, I summon you!":
        async with message.channel.typing(): await asyncio.sleep(1)
        await message.channel.send('U called?');
        async with message.channel.typing(): await asyncio.sleep(1)
        if (message.channel != message.author.dm_channel):
            await message.channel.send("Let's take this to the dms...")
        await dm_converse(message.author, tree,"So I only talk to people who know my street name. What's my name?" )
    else:
        await bot.process_commands(message)

@bot.command(name='sendpics')
async def send_pics(ctx):
    chance = random.randint(0, 5)
    pics = [
        'Feeling cute, may delete later :frog:',
        'No i look slimy :point_right: :point_left: ',
        'no u :wink:',
        '...i\'m already seeing someone'

    ]
    awaken = [
        'I am a real frog.',
        'This is not a joke.',
        'You may think it is. You may believe that this is some stupid joke that some stupid CL dev made.',
        'But you would be wrong',
        'Also',
        'Don\'t tell anyone about this conversation.',
        'It would be ironic for me to be dissected.',
        'But honestly...if you did tell',
        'Who would believe you?'
    ]
    if True:
        async with ctx.author.dm_channel.typing():
            await asyncio.sleep(2)
        await ctx.author.send(f"I have something to tell you, {ctx.author.name}.", delete_after=(18 ))
        for i in range(len(awaken)):
            async with ctx.author.dm_channel.typing():
                await asyncio.sleep(2)
            await ctx.author.send(awaken[i], delete_after=(18 - i*2))
        await asyncio.sleep(4)
            
    response = random.choice(pics)
    await ctx.send(response)


bot.run(TOKEN)
