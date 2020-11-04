import os

import discord
from dotenv import load_dotenv
from discord.ext import commands

import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix = '!')

# Print in terminal when the bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# Binary vote
@bot.command(name="bin_vote")
async def bin_vote(ctx, *text):
    # print text
    message = await ctx.send(" ".join(text))

    # add emote
    await message.add_reaction("\U00002705")
    await message.add_reaction("\U0000274C")

    # Delete the command message
    await ctx.message.delete()

# Clear command
@bot.command(name="clear")
async def clear(ctx):
    await ctx.send("############################################################")
    await ctx.send("                          CLEAR                             ")
    await ctx.send("############################################################")

    # Delete the command message
    await ctx.message.delete()


# Real bot
stick = 23
is_running = False
user_id = 0
@bot.event
async def on_message(message):
    global stick
    global is_running
    global user_id

    # Show help
    if message.content == "help nim":
        await message.channel.send("To start a game : \"start nim\"")
        await message.channel.send("To end a game : \"stop\"")
        await message.channel.send("To show the state of the bot : \"state\"")
        await message.channel.send("When the game is active type a number between 1 and 3 to delete stick")

    # Show the state of bot
    if message.content == "state":
        if user_id:
            name = bot.get_user(user_id).name
            await message.channel.send("{} is playing".format(name))
        else:
            await message.channel.send("Nobody is playing")
        
    # Start the party
    if message.content == "start nim":
        # if is not running then begin the party
        if not is_running:
            stick = 23
            is_running = True
            user_id = message.author.id
            await message.channel.send("Start with {} sticks\nYou must enter a number between 1 and 3 :".format(stick))
        # if it's the player
        elif message.author.id == user_id:
            stick = 23
            is_running = True
            user_id = message.author.id
            await message.channel.send("Start with {} sticks\nYou must enter a number between 1 and 3 :".format(stick))
        # if it's not the player
        else:
            await message.channel.send("It's not your time {}.".format(message.author.name))

    # Stop the party
    if is_running and message.content == "stop":
        # f it's the player
        if message.author.id == user_id:
            is_running = False
            user_id = 0
            await message.channel.send("You stop the party, see you soon.")
        # if it's not the player
        else:
            await message.channel.send("It's not your time {}.".format(message.author.name))


    # Handle sticks
    if message.author.id == user_id and is_running and (message.content == "1" or message.content == "2" or message.content == "3"): 

        number = int(message.content)
        stick -= number

        # display
        await message.channel.send("Your play : {}".format(number))
        
        if stick < 1:
            await message.channel.send("You lost !!!")
            is_running = False
            user_id = 0
            return
        
        await message.channel.send("There are {} sticks left !!!".format(stick))
        
        # simple ia whick get ramdom value
        ia = random.randrange(1, 3)
        stick -= ia

        # display
        await message.channel.send("IA play : {}\n".format(ia))
        
        if stick < 1:
            await message.channel.send("You win !!!")
            is_running = False
            user_id = 0
            return


        await message.channel.send("There are {} sticks left !!!".format(stick))

# Run the bot
bot.run(TOKEN)
