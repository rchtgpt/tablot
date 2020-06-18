<h1 align="center">Tablot</h1>

<p align="center">
  <a href="https://discord.gg/6mtRwdn">
    <img src="https://badgen.net/badge/discord/join%20chat/7289DA?icon=discord" alt="Discord Server" />
  </a>
</p>

whenever someone sends a public google sheets link in the server, Tablot takes the google sheet data and displays it in the form of a table.

we currently use <a href='https://pypi.org/project/terminaltables/'>terminaltables</a> to generate the table.

we are working on this just for the sake of getting familiarized with <a href='https://discordpy.readthedocs.io/en/latest/'>discord.py</a>

## why tablot?
> It's like one of those small things that makes your life 1% easier <3
> ~ clash

## commands

#### about
command: `$ts about` <br>
action: bot introduces itself

#### ping
command: `$ts stats`<br>
action: returns bot latency in `ms`

#### full gsheet
command: `$ts show "<google sheet link>"`<br>
action: displays the whole table

### gsheet specific value
command: `$ts show "<google sheet link>" value`<br>
action: displays rows corresponding to the specific value

## building from source
Install everything written in `requirements.txt` with pip install.

`cd` to `tablot` directory.

Create `.env` file and fill it with token

`BOT_TOKEN=<your token>`