import discord
from discord.ext import commands
import random
import Model.MessageCommand as mmc

description = '''
An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

bot = commands.Bot(command_prefix='_', description=description)

mc = mmc.MCommand(bot)

voice = None

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_message(message):
    if message.content.startswith('_'):
        await bot.process_commands(message)
    else:
        await mc.command(message.content, message)

@bot.command(pass_context=True, no_pm=True)
async def join(ctx, *, message: str):
    channel = discord.utils.get(bot.get_all_channels(), server__name=ctx.message.channel.server.name, name=message)
    try:
        voice = bot.join_voice_channel(channel)
    except discord.ClientException:
        await print('Already in a voice channel...')
    except discord.InvalidArgument:
        await print('This is not a voice channel...')

    await bot.delete_message(ctx.message)

@bot.command()
async def add(left : int, right : int):
    """Adds two numbers together."""
    await bot.say(left + right)

@bot.command()
async def roll(dice : str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await bot.say('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say(result)

@bot.command(description='For when you wanna settle the score some other way')
async def choose(*choices : str):
    """Chooses between multiple choices."""
    await bot.say(random.choice(choices))

@bot.command()
async def repeat(times : int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await bot.say(content)

@bot.command()
async def joined(member : discord.Member):
    """Says when a member joined."""
    await bot.say('{0.name} joined in {0.joined_at}'.format(member))

@bot.group(pass_context=True)
async def cool(ctx):
    """Says if a user is cool.

    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await bot.say('No, {0.subcommand_passed} is not cool'.format(ctx))

@cool.command(name='bot')
async def _bot():
    """Is the bot cool?"""
    await bot.say('Yes, the bot is cool.')


bot.run('YOUR_BOT_TOKEN')
