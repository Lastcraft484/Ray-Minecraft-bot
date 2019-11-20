import discord
from discord.ext import commands
from mcstatus import MinecraftServer
import config
import aiohttp

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def coord(ctx):
    with open('coords.txt') as f:
        await ctx.send(f.read())

@bot.command()
async def server(ctx):
        
    server = MinecraftServer.lookup('(remove parentheses and put ip here)')
    status = server.status()
    
    await ctx.send("The server has {0} players and replied in {1} ms".format(status.players.online, status.latency))

@bot.command()
async def coords(ctx, xCoord: str, yCoord: str, zCoord: str, nameCoord: str = None):
    if not xCoord or not yCoord or not zCoord or not nameCoord:
        await ctx.send(ctx.message.author.mention + ' You are missing some information.\nFormat: ?coords x y z name')
        return
    try:      
        await ctx.send("You submitted {} located at {},{},{}".format(nameCoord, xCoord, yCoord, zCoord))
        with open('coords.txt','a') as f:
           f.write(f'{xCoord} {yCoord} {zCoord} {nameCoord}\n')
    except Exception as e:
        print(e)
        await ctx.send("Something went wrong.")

bot.command()
async def reqcoord(ctx, *, search):
    with open('coords.txt') as f:
        for line in f:
            if line.endswith(f'{search}\n'):
                await ctx.send(line)
                break
            
        else:
                
                await ctx.send("No Coords Have Been Recorded Of That Location")

if __name__ == '__main__':
    import config
    bot.run(config.token)