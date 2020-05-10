import discord
from discord.ext import commands
from yeelight import Bulb
from yeelight.transitions import *
from yeelight import Flow
import json
import webcolors

class Light(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.config = json.load(open('config.json', 'r'))
        self.lights = json.load(open('cogs/lights.json', 'r'))

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Light cog online')
        await self.client.get_channel(self.config['logChannel']).send('Yeelight cog ready')

    async def getLightStatus(self, light):
        bulb = Bulb(self.lights[0]['ip'])
        bulbProps = bulb.get_properties()
        return bulbProps


    async def lightEventMsg(self, ctx, msg):
        embed = discord.Embed(description=msg)
        await ctx.send(embed=embed)
        return

    # Commands
    @commands.command()
    async def off(self, ctx):
        names = []
        for light in self.lights:
            try:
                Bulb(light['ip'], effect="smooth", duration=1500).turn_off()
            except AssertionError as err:
                await ctx.send(err)
                return
            names.append(light['name'])
        successMsg = ", ".join(names)
        await self.lightEventMsg(ctx, f'Turned off **{successMsg}**')

    @commands.command()
    async def on(self, ctx):
        names = []
        for light in self.lights:
            try:
                Bulb(light['ip'], effect="smooth", duration=1500).turn_on()
            except AssertionError as err:
                await ctx.send(err)
                return
            names.append(light['name'])
        successMsg = ", ".join(names)
        await self.lightEventMsg(ctx, f'Turned on **{successMsg}**')

    @commands.command()
    async def toggle(self, ctx):
        names = []
        for light in self.lights:
            try:
                Bulb(light['ip'], effect="smooth", duration=1500).toggle()
            except AssertionError as err:
                await ctx.send(err)
                return
            names.append(light['name'])
        successMsg = ", ".join(names)
        await self.lightEventMsg(ctx, f'Toggled **{successMsg}**')

    @commands.command()
    async def ct(self, ctx, arg):
        if not int(arg):
            await ctx.send('Please provide colour temperature as a number')
            return
        arg = int(arg)
        if (arg < 1700) or (arg > 6500):
            await ctx.send('Colour temperature must be between 1700 and 6500')
            return
        names = []
        for light in self.lights:
            try:
                Bulb(light['ip'], effect="smooth", duration=1500).set_color_temp(arg)
            except AssertionError as err:
                await ctx.send(err)
                return
            names.append(light['name'])
        successMsg = ", ".join(names)
        await self.lightEventMsg(ctx, f'Set colour temperature of **{successMsg}** to {str(arg)}')

    @commands.command()
    async def bright(self, ctx, arg):
        if not int(arg):
            await ctx.send('Please provide brightness as a number')
            return
        arg = int(arg)
        if (arg < 1) or (arg > 100):
            await ctx.send('Brightness must be between 1 and 100')
            return
        names = []
        for light in self.lights:
            try:
                Bulb(light['ip'], effect="smooth", duration=1500).set_brightness(arg)

            except AssertionError as err:
                await ctx.send(err)
                return
            names.append(light['name'])
        successMsg = ", ".join(names)
        await self.lightEventMsg(ctx, f'Set brightness **{successMsg}** to {str(arg)}')

    @commands.command()
    async def hsv(self, ctx, *arg):
        for args in arg:
            if (not int(args)):
                await ctx.send('Please provide values as a number')
                return
        if len(arg) == 3:
            arg1,arg2,arg3 = arg
        if len(arg) == 2:
            arg1,arg2 = arg
        arg1 = int(arg1)-1
        if (arg1 < 0) or (arg1 > 360):
            await ctx.send('Hue must be between 0 and 360')
            return
        names = []
        for light in self.lights:
            try:
                Bulb(light['ip'], effect="smooth", duration=1500).set_hsv(arg1, arg2, arg3)
            except AssertionError as err:
                await ctx.send(err)
                return
            names.append(light['name'])
        successMsg = ", ".join(names)
        await self.lightEventMsg(ctx, f'Set HSV on **{successMsg}**')

    @commands.command()
    async def colour(self, ctx, *arg):
        if len(arg) > 3:
            await ctx.send('You did something wrong fam')
            return
        if len(arg) == 3: # must be rgb numbers!
            try:
                red,green,blue = arg
            except ValueError as err:
                await ctx.send(err)
                return
        if (len(arg) == 1) and (arg[0].startswith('#')): # this is a hex value
            try:
                red, blue, green = webcolors.hex_to_rgb(arg[0])
            except ValueError as err:
                await ctx.send(err)
                return
        if (len(arg) == 1) and (not arg[0].isdigit()): # must be colour name
            try:
                listArg = list(arg) # nametorgb attempts to lower arg, so needs to /not/ be a tuple
                red, green, blue = webcolors.name_to_rgb(listArg, spec='css3')
            except ValueError as err:
                await ctx.send(err)
                return
        names = []
        for light in self.lights:
            try:
                Bulb(light['ip'], effect="smooth", duration=1500).set_rgb(red, green, blue)
            except AssertionError as err:
                await ctx.send(err)
                return
            names.append(light['name'])
        successMsg = ", ".join(names)
        await self.lightEventMsg(ctx, f'Set colour to \({red}, {green}, {blue}\) on **{successMsg}**')

    @commands.command()
    async def disco(self, ctx):
        flow = Flow(
            count=10,
            transitions=disco(),
        )
        names = []
        for light in self.lights:
            try:
                Bulb(light['ip'], effect="smooth", duration=1500).start_flow(flow)
            except AssertionError as err:
                await ctx.send(err)
                return
            names.append(light['name'])
        successMsg = ", ".join(names)
        await self.lightEventMsg(ctx, f'Enabled party mode on **{successMsg}**')

def setup(client):
    client.add_cog(Light(client))