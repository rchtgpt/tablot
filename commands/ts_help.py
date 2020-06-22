import discord
client = discord.Client()

def help():
    embed = discord.Embed(
        title="Tablot's commands:",
        colour=1499502,
        description="""
> To use a command, type `$ts <command>`.

**__General__**

`about` - To know about the bot.
`stats` - To check the bot's stats.

**__Google Sheets__**

Using google sheet link:

`show "<link>"` - To display the whole table
`show "<link>" row value` - To display rows belonging to a specific value
`show "<link>" col value` - To display a specific column

Using owner defined link variable:

`link "<link>" linkVariable` - To assign a variable to the link (*only server owner*)
`show linkVariable` - To display the table stored in the link variable
`show linkVariable row value` - To display rows of specific value
`show linkVariable col value` - To display a specific column
""").set_footer(text='Made by Tech Syndicate', icon_url='https://techsyndicate.co/img/logo.png')
    
    return embed