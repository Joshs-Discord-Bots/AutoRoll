import nextcord, psutil, asyncio, time, requests, subprocess
from nextcord.ext import commands

class Stats(commands.Cog):
    def __init__(self, client):
        self.client = client
        return

    async def checkBattery(self, client, limit):
        '''
        limit = Minimum Battery Limit
        '''
        flag = False
        while True:
            battery = psutil.sensors_battery()
            if battery and (battery.percent < limit and not flag):
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



    @commands.Cog.listener()
    async def on_ready(self):
        self.client.startTime = time.time()
        await self.client.get_user(self.client.admins[0]).send(f'{self.client.user.mention} has connected to Discord! ({self.formatTime(self.client.startTime)})')
        await self.checkBattery(self.client, limit=15)
        return



    @nextcord.slash_command(description='Display Host Machine Stats')
    async def stats(self):
        return

    @stats.subcommand(description='Returns all bot metrics.')
    async def all(self, interaction : nextcord.Interaction):
        await self.uptime(interaction)
        await self.battery(interaction)
        await self.ip(interaction)
        return


    @stats.subcommand(description='Will return the bot\'s IP')
    async def ip(self, interaction : nextcord.Interaction):
        if not self.client.admin(interaction.user):
            await interaction.send('You do not have permission to use this command!')
            return

        pubIP = requests.get('https://ifconfig.me').content.decode('utf-8')
        privIP = subprocess.check_output("hostname -I | awk '{print $1}'", shell=True).decode().replace('\n','')

        embed = nextcord.Embed(title='Server IP 💻', colour=nextcord.Colour.blue())
        embed.add_field(name='Public', value=f'`{pubIP}`', inline=False)
        embed.add_field(name='Private', value=f'`{privIP}`', inline=False)
        await interaction.send(embed=embed, ephemeral=True)
        return



    @stats.subcommand(description='Will return the battery of the bot.')
    async def battery(self, interaction : nextcord.Interaction):
        battery = psutil.sensors_battery()
        colour = nextcord.Colour.green() if battery and battery.percent > 15 else nextcord.Colour.red()

        embed = nextcord.Embed(title="Server Battery Stats", colour=colour)
        if not battery:
            embed.add_field(name='Error', value='`Battery status is unavailable`', inline=False)
        else:
            embed.add_field(name='Battery percentage:', value=f'`{round(battery.percent, 2)}%`', inline=False)
            embed.add_field(name='Power plugged in:', value=f'`{battery.power_plugged}`', inline=False)
            embed.add_field(name='Battery time remaining:', value=f'`{self.convertSeconds(battery.secsleft)}`', inline=False)
        await interaction.send(embed=embed)
        return

    @stats.subcommand(description='Will return the bot\'s Uptime')
    async def uptime(self, interaction : nextcord.Interaction):
        uptime = self.convertSeconds(time.time() - self.client.startTime)
        embed = nextcord.Embed(title=f"{self.client.user.name} Uptime ⌛", colour=nextcord.Colour.blue())
        embed.add_field(name='Start Time:', value=f'`{self.formatTime(self.client.startTime)}`', inline=False)
        embed.add_field(name='Uptime:', value=f'`{uptime}`', inline=False)
        await interaction.send(embed=embed)
        return
        
def setup(client):
    client.add_cog(Stats(client))
    return
