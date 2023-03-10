<p align="center">
  <img src="https://github.com/Joshs-Discord-Bots/AutoRoll/blob/main/src/cogs/resources/Icons/Bot%20Profile%20Pic.jpg" width="128" height="128">
</p>

<h1 align="center">AutoRoll Discord Bot</h1>

## About
Little passion project of mine :)
A discord bot that can (hopefully) do a little bit of everything!

### .env file format (REQUIRED)
```env
############################ General ############################ 

# Bot Token
TOKEN=""
# Optional development bot token (used for simultaneous development)
DEVTOKEN=""
# Setting this to TRUE will run the bot using the DEVTOKEN specified above
DEVMODE=FALSE
# Set bot's legacy command prefix
PREFIX="$"
# List of admin IDs for admin-only bot commands (CSV)
ADMINS=""

############################ Intents ############################ 

MESSAGES=FALSE
MEMBERS=FALSE
GUILDS=FALSE
VOICE_STATES=FALSE
```