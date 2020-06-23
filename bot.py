import discord
import os
from terminaltables import AsciiTable
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import firebase_admin
from firebase_admin import credentials, firestore
from commands.ts_about import about
from commands.ts_show_var import return_doc
from commands.ts_show_var import show_var
from commands.ts_show_var import show_var_row
from commands.ts_show_var import show_var_col
from commands.ts_show_link import display_row
from commands.ts_show_link import display_col
from commands.ts_show_link import display_link
from commands.ts_stats import stats
from commands.ts_help import help, help_owner
from commands.ts_introduce import intro
from commands.ts_all import all_vars

client = discord.Client()
prefix = '$ts'
d = {}
sheetVar = ''
link = ''

scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]

cred = {
    "type": os.environ.get('TYPE'),
    "project_id": os.environ.get('PROJECT_ID'),
    "private_key_id": os.environ.get('PRIVATE_KEY_ID'),
    "private_key": os.environ.get('PRIVATE_KEY').replace('\\n', '\n'),
    "client_email": os.environ.get('CLIENT_EMAIL'),
    "client_id": os.environ.get('CLIENT_ID'),
    "auth_uri": os.environ.get('AUTH_URI'),
    "token_uri": os.environ.get('TOKEN_URI'),
    "auth_provider_x509_cert_url": os.environ.get('AUTH_PROVIDER_CERT_URL'),
    "client_x509_cert_url": os.environ.get('CLIENT_CERT_URL')
}

firebase_admin.initialize_app(credentials.Certificate(cred))
db = firestore.client()
creds = ServiceAccountCredentials.from_json_keyfile_dict(cred)
gClient = gspread.authorize(creds)
start_time = 0

@client.event
async def on_ready():
    print('i\'m ready to get back to work')
    global start_time
    start_time = time.time()
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you type $ts"))


@client.event
async def on_guild_join(guild):
    if guild.system_channel == None:
        try:
            channel = discord.utils.get(guild.text_channels, name="general")
            embed = about()
            await channel.send(embed=embed)
        except:
            embed = about()
            await guild.channel.send(embed=embed)
    else:
        embed = about()
        await guild.system_channel.send(embed=embed)


@client.event
async def on_member_join(member):
    try:
        guild_name = member.guild
        guild_owner = member.guild.owner
        owner = member.guild.owner.id
        await member.create_dm()
        await member.dm_channel.send(
            f'''Hey {member.name}, welcome to the official server of {guild_name}

To use the various channels of {guild_name}, please introduce yourself in `#introductions` using the format given below.
        ```
$ts introduce
name: "name"
school: "school_name"
event: "event_name"
email: "email_id" ```
        '''
        )
        checker = False
        for c in member.guild.channels:
            if 'introductions' in c.name:
                checker = True
                break
        if not checker:
            await member.create_dm()
            await member.dm_channel.send(
                f'<@{owner}> is creating `#introductions` pls be patient'
            )
            await guild_owner.create_dm()
            await guild_owner.dm_channel.send(
                f'<@{owner}>, ik you\'re cool but u might wanna create `#introductions` in {guild_name}'
            )
    except Exception as e:
        print(e)

@client.event
async def on_message(message):

    if message.content.startswith(f'{prefix} introduce') and str(message.channel) == 'introductions':
        sheet = gClient.open_by_url("https://docs.google.com/spreadsheets/d/1rCIv4UG3s1QFhCOZFMNmVraksTVCILhCukL6dnaW0vA/edit?usp=sharing").sheet1
        indi = message.content.split('\n')[1:]
        introd = intro(indi, db, message.guild.id, message.author, message.author.id, sheet)
        if introd == 'add':
            await message.channel.send("Information added successfully :grinning:")
        else:
            await message.channel.send("Information updated successfully :grinning:")
        user = message.author
        try:
            await user.add_roles(discord.utils.get(user.guild.roles, name='test'))
        except Exception:
            if introd == 'add':
                await message.channel.send(
                    f'<@{message.guild.owner.id}>, pls add the bot role above the desired role to be given')

    if message.content.startswith(f'{prefix} link'):
        if message.author == message.guild.owner:
            a = message.content.split('"')
            if len(a) == 3 and a[-1] != '':
                j = a[1]
                if j[1] == '<' and j[-1] == '>':
                    try:
                        try_sheet = gClient.open_by_url(a[1][1:-1]).sheet1
                        from commands.ts_link import link
                        sheetVar = link(a, db, message.guild.id)
                        await message.channel.send(f'the assigned variable is `{(str(sheetVar))}`')
                    except Exception:
                        await message.channel.send(
                            'The command syntax is incorrect. Please use `$ts help` to check the commands.')
                else:
                    await message.channel.send("i think you forgot to put '<' and '>' before and after your link :thinking:")
            else:
                await message.channel.send(
                    'The command syntax is incorrect. Please use `$ts help` to check the commands.')
        else:
            await message.channel.send(f'this command is only for <@{message.guild.owner.id}>. pls don\'t use it. kthxbye.')

    if f'{prefix} show' in message.content and '"' not in message.content:
        doc = return_doc(db, message.guild.id)
        try:
            for var in doc:
                if message.content == f'{prefix} show {var}':
                    table = show_var(gClient, doc, var)
                    await message.channel.send(f'```{table.table}```')

                elif f'{prefix} show {var} row' in message.content or f'{prefix} show {var} --r' in message.content:
                    a = message.content.split(" ", 4)
                    sheet = gClient.open_by_url(doc[var]).sheet1
                    data = sheet.findall(a[-1])
                    if len(data) < 1:
                        await message.channel.send(f'i\'m unable to find `{a[-1]}` in {var} :thinking:')
                    else:
                        for final in show_var_row(a, gClient, doc, var):
                            await message.channel.send(f'```{final}```')

                elif f'{prefix} show {var} col' in message.content or f'{prefix} show {var} --c' in message.content:
                    a = message.content.split(" ", 4)
                    lst = show_var_col(a, gClient, doc, var)
                    if lst == 'error':
                        await message.channel.send('bro this column doesn\'t exist, please recheck :sweat_smile:')
                    else:
                        await message.channel.send(f'```{AsciiTable(lst).table}```')
        except:
            await message.channel.send('variable not found. pls assign a sheet link to it')

    if message.content.startswith(f'{prefix} show ') and '"' in message.content:
        if message.content[-1] != '"':
            a = message.content.split('"')
            if len(a) < 3:
                await message.channel.send(
                    'The command syntax is incorrect. Please use `$ts help` to check the commands.')
            else:
                try:
                    link = a[1][1:-1]
                    if message.content.startswith(f'{prefix} show "<{link}>" row ') or message.content.startswith(f'{prefix} show "<{link}>" --r '):
                        sheet = gClient.open_by_url(link).sheet1
                        j = message.content.split(" ", 5)
                        data = sheet.findall(j[-1])
                        if len(data) < 1:
                            await message.channel.send(f'i\'m unable to find `{j[-1]}` in <{link}> :thinking:')
                        else:
                            for final in display_row(gClient, link, message.content):
                                await message.channel.send(f'```{final}```')
                                
                    elif message.content.startswith(f'{prefix} show "<{link}>" col ') or message.content.startswith(f'{prefix} show "<{link}>" --c '):
                        j = message.content.split(" ", 5)
                        lst = display_col(gClient, j, link)
                        if lst == 'error':
                            await message.channel.send('bro this column doesn\'t exist, please recheck :sweat_smile:')
                        else:
                            await message.channel.send(f'```{AsciiTable(lst).table}```')
                except:
                    await message.channel.send(
                        'Please enter a valid google sheet link. Also, if you haven\'t already, please share your google sheet with `techsyndicate@tablot-280818.iam.gserviceaccount.com`.')

        else:
            try:
                a = message.content.split('"')
                link = a[1]
                if link[1] == '<' and link[-1] == '>':
                    link = a[1][1:-1]
                    if link.startswith('https://docs.google.com/spreadsheets/d/'):
                        table = display_link(gClient, link)
                        await message.channel.send(f'```{table.table}```')
                    else:
                        await message.channel.send('Please enter a valid google sheet link. Also, if you haven\'t already, please share your google sheet with `techsyndicate@tablot-280818.iam.gserviceaccount.com`.')
                else:
                    await message.channel.send("i think you forgot to put '<' and '>' before and after your link :thinking:")
            except Exception as e:
                await message.channel.send(
                    'Please enter a valid google sheet link. Also, if you haven\'t already, please share your google sheet with `techsyndicate@tablot-280818.iam.gserviceaccount.com`.')

    if message.content == f'{prefix} all':
        try:
            var = all_vars(db, message.guild.id)
            await message.channel.send(f'```{var}```')
        except:
            await message.channel.send('mate at least add some variables first :sweat:')
    
    if message.content == prefix:
        embed = about()
        await message.channel.send(embed=embed)

    if message.content.startswith(f'{prefix} stats'):
        name_list = set()
        for g in client.guilds:
            for s in g.members:
                name_list.add(s.name)
        latency = round(client.latency * 1000, 2)
        embed = stats(start_time, time.time(), name_list, latency, client.guilds)
        await message.channel.send(embed=embed)

    if message.content == f'{prefix} help':
        embed = help()
        await message.channel.send(embed=embed)

    elif message.content == f'{prefix} help owner':
        if message.author == message.guild.owner:
            embed = help_owner()
            await message.channel.send(embed=embed)
        else:
            await message.channel.send(f'this command is only for <@{message.guild.owner.id}>. pls leave me alone :sweat_smile:')


client.run(os.environ.get('TOKEN'))

# email: techsyndicate@tablot-280818.iam.gserviceaccount.com
