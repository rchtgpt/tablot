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

### general commands

**about**
command: `$ts about` <br>
action: bot introduces itself

**ping**
command: `$ts stats`<br>
action: returns bot latency in `ms`


### gsheet commands

#### using google sheets link

**full gsheet using gsheet link**
command: `$ts show "<google sheet link>"`<br>
action: displays the whole table

**gsheet link specific rows**
command: `$ts show "<google sheet link>" row value`<br>
action: displays rows belonging to the specified value

**gsheet link specific columns**
command: `$ts show "<google sheet link>" col value`<br>
action: displays a specific column using column name

#### using owner defined link variable

**assign name to gsheet link (only the *owner* can do)**
command: `$ts link <"link"> linkVariable`<br>
action: assigns a name to the link provided by the owner

**full gsheet using owner defined link variable**
command: `$ts show variableName` <br>
action: displays the whole table

**gsheet linkVariable specific rows**
command: `$ts show linkVariable row value`<br>
action: displays rows belonging to the specified value

**gsheet link specific columns**
command: `$ts show linkVariable col value`<br>
action: displays a specific column using column name as value


## building from source
Install everything written in `requirements.txt` with pip install.

`cd` to `tablot` directory.

change `cred` variable value to your `creds.json` values

also put your discord bot token inside `client.run()`