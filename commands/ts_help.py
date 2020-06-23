import discord
client = discord.Client()

def help():
    embed = discord.Embed(
        title="Tablot's commands:",
        colour=1499502,
        description="""
        
**__General__**

`$ts` - To know about the bot.
`$ts stats` - To check the bot's stats.

**__Google Sheets__**

Using google sheet link:

`$ts show "<link>"` - To display the whole table
`$ts show "<link>" row value` - To display rows belonging to a specific value (use `--r` instead of row)
`$ts show "<link>" col value` - To display a specific column (use `--c` instead of col)

Using owner defined link variable:

`$ts link "<link>" linkVariable` - To assign a variable to the link (*only server owner*)
`$ts show linkVariable` - To display the table stored in the link variable
`$ts show linkVariable row value` - To display rows of specific value (use `--r` instead of row)
`$ts show linkVariable col value` - To display a specific column (use `--c` instead of col)
""").set_footer(text='Made by Tech Syndicate', icon_url='https://techsyndicate.co/img/logo.png')
    
    return embed

def help_owner():
    embed = discord.Embed(
        title="Tablot's owner specific commands:",
        colour=1499502,
        description="""
***dw i'm here to help you***

`$ts link "<link>" linkVariable` - to assign a variable name to your google sheet link
`$ts event sheet "<link>"` - give an empty sheet (todo) (intros will be updated here)
`$ts intro format` - define the intro headings
""").set_footer(text='Made by Tech Syndicate', icon_url='https://techsyndicate.co/img/logo.png')

    return embed