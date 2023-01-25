import nextcord, os, platform, json, psutil, asyncio, time
from nextcord.ext import commands

class Stats(commands.Cog):
    def __init__(self, client):
        self.client = client
        return

    async def checkBattery(self, client, limit):
        flag = False
        while True:
            battery = psutil.sensors_battery()
            if battery.percent < limit and not flag:
                print('battery is at ', battery.percent)
                flag = True
                pings = ' '.join(str(client.get_user(user).mention) for user in client.admins)
                await client.get_channel(899734389724942396).send(f'{pings} Battery is low! Please charge me!')
            else:
                flag = False
            await asyncio.sleep(300)

    def convertSeconds(self, seconds):
        days, seconds = divmod(seconds, 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)
        time_str = ""
        if days > 0: time_str += f"{round(days)}d "
        if hours > 0: time_str += f"{round(hours)}h "
        if minutes > 0: time_str += f"{round(minutes)}m "
        if seconds > 0: time_str += f"{round(seconds)}s"
        return time_str

    def formatTime(self, timestamp):
        return time.strftime("%d/%m/%Y %H:%M:%S", time.gmtime(timestamp + 8 * 3600))



    async def on_ready():
        await self.client.get_user(285311305253126145).send(f'{client.user.mention} has connected to Discord!\n{formatTime(client.startTime)}')



    @nextcord.slash_command(description='Add/Remove roles')
    async def stats(self):
        return
    
    @stats.subcommand(description='Will return the battery of the bot.')
    async def battery(interaction : nextcord.Interaction):
        battery = psutil.sensors_battery()
        colour = nextcord.Colour.green() if battery.percent > 15 else nextcord.Colour.red()

        embed = nextcord.Embed(title="Server Battery Stats", colour=colour)
        embed.add_field(name='Battery percentage:', value=f'`{round(battery.percent, 2)}%`', inline=False)
        embed.add_field(name='Power plugged in:', value=f'`{battery.power_plugged}`', inline=False)
        embed.add_field(name='Battery time remaining:', value=f'`{self.convertSeconds(battery.secsleft)}`', inline=False)
        await interaction.send(embed=embed)
        return

    @stats.subcommand(description='Will return the bot\'s Uptime')
    async def uptime(interaction : nextcord.Interaction):
        uptime = convertSeconds(time.time() - client.startTime)
        embed = nextcord.Embed(title=f"{client.user.name} Uptime ⌛", colour=nextcord.Colour.blue())
        embed.add_field(name='Start Time:', value=f'`{formatTime(client.startTime)}`', inline=False)
        embed.add_field(name='Uptime:', value=f'`{uptime}`', inline=False)
        await interaction.send(embed=embed)
        return
        
def setup(client):
    client.add_cog(Stats(client))
    return