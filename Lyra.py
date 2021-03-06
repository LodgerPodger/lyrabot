import asyncio
import sys
import os.path

import discord
from discord.ext import commands

STAR = 410660094083334155
PERS = 347100862125965312

METAEXTENSION = "cogs.meta"

owners = [PERS]
owners = set(owners)

client = commands.Bot(command_prefix = '!', owner_ids = owners)

status = True

############################################## EVENTS ##############################################

@client.event
async def on_ready():
    print("Lyra is online")

@client.event
async def on_resumed():
    print("Lyra has reconnected")

@client.event
async def on_command_error(ctx, err):
    if isinstance(err, commands.CommandOnCooldown):
        await ctx.channel.send("You're on cooldown, " + ctx.author.display_name)
    elif isinstance(err, commands.CommandNotFound):
        await ctx.channel.send("I don't think that's something I can do...")
    else:
        print("--- caught " + err.__class__.__name__ + " ---\n" + str(err))
        await ctx.channel.send("Something bad happened! I can't do that, sorry.")

@client.event
async def on_member_remove(member):
    lyra = None
    for channel in member.guild.channels:
        if channel.name == "lyra":
            lyra = channel
    if lyra is not None:
        await lyra.send(member.display_name + ' has left the server')
    else:
        print(member.display_name + "left server: " + member.guild)

@client.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name = 'everypony')
    if role:
        await member.add_roles(role)

############################################## COMMANDS ##############################################


@client.command()
@commands.cooldown(2, 7, commands.BucketType.user)
async def bon(ctx):
    """ bon """
    await ctx.channel.send('bon')

@client.command()
async def dm(ctx):
    """ also bon """
    await ctx.message.author.send("bon")

@client.command()
async def nuke(ctx, *args):
    """ :dab: """
    author = ctx.author
    if author.guild_permissions.administrator:
        msg = ""
        for i in range(10):
            msg += "<:dab:531755608467046401>\n"
        for i in range(5):
            await ctx.channel.send(msg)
    else:
        await ctx.channel.send("You're gonna have a bad time. Might need more perms for that!")

@client.command()
async def snuggle(ctx):
    """ for snugs """
    if ctx.message.author.id != STAR:
        return
    global status
    if status:
        status = not status
        await client.change_presence(activity=discord.Game('with some faggo'))
    else:
        status = not status
        await client.change_presence(activity=discord.Game('her lyre'))

@client.command()
async def rest(ctx, *args):
    """ For when lyra gets tired """
    if ctx.author.id in owners:
            sleepytwi = discord.utils.get(client.emojis, name = 'sleepytwi')
            if sleepytwi:
                await ctx.channel.send(sleepytwi)
            else:
                await ctx.channel.send("Alright. Nighty-night!")
            await client.close()
            print('Lyra is offline')
    else:
        await ctx.channel.send("Aww, but I'm not tired yet!")
        

############################################## RUNNING ##############################################

def get_token():
    tokenloc = "token.txt"
    if len(sys.argv) > 1:
        token = sys.argv[1]
        if not os.path.isfile(tokenloc):
            with open(tokenloc, "w") as tokenfile:
                tokenfile.write(token)
    else:
        if os.path.isfile(tokenloc):
            with open(tokenloc, "r") as tokenfile:
                token = tokenfile.readline().strip()
        else:
            raise Exception("Could not find token")
    return token

def load_meta():
    try:
        client.load_extension(METAEXTENSION)
    except Exception as e:
        print('meta extension could not be loaded. [{}]'.format(extension, e))
        raise e

def main():
    token = get_token()
    load_meta()

    client.run(token)

    print("Closing client")
    try:
        client.close().send(None)
    except StopIteration:
        print("All done!")
    sys.exit()


if __name__ == "__main__":
    main()
