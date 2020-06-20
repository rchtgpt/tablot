import discord
import os
from terminaltables import AsciiTable
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime, time

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

creds = ServiceAccountCredentials.from_json_keyfile_dict(cred)
gClient = gspread.authorize(creds)
start_time = 0

@client.event
async def on_ready():
    print('i\'m ready to get back to work')
    global start_time
    start_time = time.time()

@client.event
async def on_member_join(member):
    try:
        guild_name = member.guild

        await member.create_dm()
        await member.dm_channel.send(
            f'''Hey {member.name}, welcome to the official server of {guild_name}
        
To use the various channels of {guild_name}, please introduce yourself in `#introduction` using the format given below.
        ```
name: "name"
school: "school_name"
event: "event_name"
email: "email_id" ```
        '''
        )

    except Exception as e:
        print(e)
    

@client.event
async def on_message(message):
    if message.content.startswith(f'{prefix} link'):
        if message.author == message.guild.owner:
            if message.content[-1] != '"':
                global sheetVar, link
                a = message.content.split('"')
                sheetVar = a[2].strip()
                link = a[1][1:-1]
                d[sheetVar] = link
                await message.channel.send(f'the assigned variable is {sheetVar}')
            else:
                await message.channel.send('The command syntax is incorrect. Please use `$ts help` to check the commands.')
        else:
            await message.channel.send(f'this command is only for {message.guild.owner}. pls don\'t use it. kthxbye.')

    for variables in d.keys():
        if message.content == f'{prefix} show {variables}':
            sheet = gClient.open_by_url(d[variables]).sheet1
            data = sheet.get_all_values()
            tableData = [data[0]]
            for i in range(1, len(data)):
                val = [k for k in data[i]]
                tableData.append(val)
            table = AsciiTable(tableData)
            await message.channel.send(f'```{table.table}```')

    if message.content.startswith(f'{prefix} show ') and '"' in message.content:
        if message.content[-1] != '"':
            a = message.content.split('"')
            if len(a) < 3:
                await message.channel.send('The command syntax is incorrect. Please use `$ts help` to check the commands.')
            else:
                try:
                    a = message.content.split('"')
                    print(a)
                    link = a[1][1:-1]
                    sheet = gClient.open_by_url(link).sheet1
                    data = sheet.findall(a[2][1:])
                    tableData = []
                    tableData.append(sheet.row_values(1))
                    for i in data:
                        tableData.append(sheet.row_values(i.row))
                    final = ''
                    for i in tableData:
                        if tableData[tableData.index(i)] == tableData[-1]:
                            break
                        else:
                            for j in range(len(i)):
                                final += f'{tableData[0][j]}: {tableData[tableData.index(i) + 1][j]}\n'
                            await message.channel.send(f'```{final}```')
                            final = ''
                except:
                    await message.channel.send('Please enter a valid google sheet link. Also, if you haven\'t already, please share your google sheet with `techsyndicate@tablot-280818.iam.gserviceaccount.com`.')

        else:
            try:
                a = message.content.split('"')
                link = a[1][1:-1]
                if link.startswith('https://docs.google.com/spreadsheets/d/'):
                    sheet = gClient.open_by_url(link).sheet1
                    data = sheet.get_all_values()
                    tableData = [data[0]]
                    for i in range(1, len(data)):
                        val = [k for k in data[i]]
                        tableData.append(val)

                    table = AsciiTable(tableData)
                    await message.channel.send(f'```{table.table}```')

                else:
                    await message.channel.send('Please enter a valid google sheet link. Also, if you haven\'t already, please share your google sheet with `techsyndicate@tablot-280818.iam.gserviceaccount.com`.')

            except Exception as e:
                await message.channel.send('Please enter a valid google sheet link. Also, if you haven\'t already, please share your google sheet with `techsyndicate@tablot-280818.iam.gserviceaccount.com`.')

    if message.content.startswith(f'{prefix} about'):
        embed = discord.Embed(title='Thanks for adding me to your server! :heart:',
                              description='To get started, simply share your google sheet with me at `techsyndicate@tablot-280818.iam.gserviceaccount.com`, and type `$ts help` for a list of commands',
                              colour=1499502) \
            .add_field(
                name='Tablot',
                value='Tablot helps you conveniently display your google sheets data on a discord server.',
                inline=False).add_field(
                name='Owner',
                value='Tech Syndicate; check us out on [GitHub](https://github.com/techsyndicate).',
                inline=False
            ).set_footer(text='Made by Tech Syndicate', icon_url='https://techsyndicate.co/img/logo.png')
        await message.channel.send(embed=embed)

    if message.content.startswith(f'{prefix} stats'):

        name_list = set()
        for g in client.guilds:
            for s in g.members:
                name_list.add(s.name)

        current_time = time.time()
        difference = int(round(current_time - start_time))

        embed = discord.Embed(
            title='Statistics',
            description='',
            colour=1499502,
        ).add_field(
            name='Guild Count',
            value=len([s for s in client.guilds]),
            inline=True
        ).add_field(
            name='User Count',
            value=len(name_list) - 1,
            inline=True
        ).add_field(
            name='Latency',
            value=f'{round(client.latency * 1000, 2)}ms',
            inline=True
        ).add_field(
            name='Uptime',
            value=datetime.timedelta(seconds=difference))\
                .set_footer(text='Made by Tech Syndicate',
                icon_url='https://techsyndicate.co/img/logo.png')
        await message.channel.send(embed=embed)

    if message.content.startswith(f'{prefix} help'):
        embed = discord.Embed(
            title="Tablot's commands:",
            colour=1499502,
            description="""
> To use a  command type `$ts <command>`.

**General:**

`about` - To know about the bot.
`stats` - To check the bot's stats.

**Google Sheets:**

`show "<google sheet link>"` - To display the whole table
`show "<google sheet link>" value` - To display rows of specific value
""").set_footer(text='Made by Tech Syndicate', icon_url='https://techsyndicate.co/img/logo.png')
        await message.channel.send(embed=embed)

client.run(os.environ.get('TOKEN'))

# email: techsyndicate@tablot-280818.iam.gserviceaccount.com
