# Racu v2

## ⚠️ Important Information

This branch is in development **and will be unstable**. The purpose of v2 is to make Racu available Discord-wide, rather than tailor-made for one server. This information below is unedited and is meant for the stable version of racu v1 (main branch).


## 🎨 Features

- XP System: Earn experience points (XP) with amusing and sometimes sarcastic level-up messages (can be disabled).
- Economy System: Engage in various economy-related activities, including:
  - Blackjack
  - Slots
  - Duels
  - Daily Rewards to keep players engaged
- Simple Moderation Module: Manage server moderation tasks.
- Currency and Level Stats: Track user currency and levels.
- Server Introductions: Automatically post server introductions in a designated channel.
- Reaction Handler: Customize bot reactions to specific messages.


## 📲 Installation
Racu is containerized: its core, database, database admin platform and logger run on Docker without any extra configuration. 
However, you CAN run it locally without Docker by hosting MariaDB on your machine with the login credentials specified in [.env](.env.template) and installing **Python 3.11** with the [required pip packages](requirements.txt). **Note: I won't explain how to do this. Figure it out on your own.**

```sh
git clone https://gitlab.com/wlinator/racu && cd racu
```

Copy `.env.template` to `.env` and fill out the [variables](#env-keys).    

**Optional:** copy `users.yml.example` to `users.yml` to properly configure Dozzle logs. Check the file for more information.  

```sh
docker compose up -d --build
```


## ⚙️ Environment variables
- `TOKEN`: your Discord Bot Token, you can get this [here](https://discord.com/developers/applications).
- `INSTANCE`: this should always be "MAIN" unless you plan to run multiple bots (for testing purposes).
- `OWNER_ID`: the Discord user ID of the person who will act as owner of this bot.
- `XP_GAIN`: a comma-seperated list of XP gain values, Racu randomly picks one on each message.
- `COOLDOWN`: a comma-seperated list of cooldown times, this is to prevent botting XP.
- The values with "DBX" can be ignored unless you plan to make database backups with Dropbox. In that case enter your Dropbox API credentials.
- `MARIADB_USER`: the username for your MariaDB database.
- `MARIADB_PASSWORD`: the password for your database.
- `MARIADB_ROOT_PASSWORD`: the root password for your database. (can be ignored unless you have a specific use for it)
