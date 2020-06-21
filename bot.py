import discord
import os
from terminaltables import AsciiTable
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime, time
import firebase_admin
from firebase_admin import credentials, firestore

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
        total = sheet.get_all_values()
        indi = message.content.split('\n')[1:]
        final_add = []
        for i in indi:
            final_add.append(i.split(":")[1].strip()[1:-1])  # to remove quotes
        final_add.append(f'{message.author}')
        col_doc = db.collection(u'registered users').document(u'{}'.format(message.guild.id))
        doc_val = col_doc.get()
        if doc_val.exists:
            doc = doc_val.to_dict()
            check = False
            for dv in doc.values():
                if message.author.id not in dv:
                    check = False
                else:
                    check = True
                    break
            if not check:
                sheet.insert_row(final_add, len(total) + 1)
                await message.channel.send("Information added successfully :grinning:")
                col_doc.update({u'ids': firestore.ArrayUnion([message.author.id])})
            else:
                all_values = sheet.get_all_values()
                for i in all_values:
                    if i[-1] == str(message.author):
                        ind = all_values.index(i)
                        break
                for i in range(1, len(final_add) + 1):
                    sheet.update_cell(ind+1, i, final_add[i-1])
                await message.channel.send("Information updated successfully :grinning:")
        else:
            add = [message.author.id]
            sheet.insert_row(final_add, len(total) + 1)
            await message.channel.send("Information added successfully :grinning:")
            db.collection(u'registered users').document(u'{}'.format(message.guild.id)).set({
                u'ids': add
            })
        user = message.author
        try:
            await user.add_roles(discord.utils.get(user.guild.roles, name='test'))
        except Exception:
            await message.channel.send(
                f'<@{message.guild.owner.id}>, pls add the bot role above the desired role to be given')

    if message.content.startswith(f'{prefix} link'):
        if message.author == message.guild.owner:
            global sheetVar, link
            a = message.content.split('"')
            if len(a) == 3 and a[-1] != '':
                try:
                    try_sheet = gClient.open_by_url(a[1][1:-1]).sheet1
                except Exception:
                    await message.channel.send(
                        'The command syntax is incorrect. Please use `$ts help` to check the commands.')
                sheetVar = a[2].strip()
                link = a[1][1:-1]
                d[sheetVar] = link
                await message.channel.send(f'the assigned variable is {sheetVar}')
            else:
                await message.channel.send(
                    'The command syntax is incorrect. Please use `$ts help` to check the commands.')
        else:
            await message.channel.send(f'this command is only for {message.guild.owner}. pls don\'t use it. kthxbye.')

    for vars in d.keys():
        if message.content == f'{prefix} show {vars}':
            a = message.content.split()
            sheet = gClient.open_by_url(d[vars]).sheet1
            data = sheet.get_all_values()
            tableData = [data[0]]
            for i in range(1, len(data)):
                val = [k for k in data[i]]
                tableData.append(val)
            table = AsciiTable(tableData)
            await message.channel.send(f'```{table.table}```')

        elif f'{prefix} show {vars} row' in message.content:
            a = message.content.split(" ", 4)
            if len(a) > 3:
                sheet = gClient.open_by_url(d[vars]).sheet1
                data = sheet.findall(a[-1])
                tableData = list()
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

        elif f'{prefix} show {vars} col' in message.content:
            a = message.content.split(" ", 4)
            if len(a) > 3:
                sheet = gClient.open_by_url(d[vars]).sheet1
                tableData = sheet.row_values(1)
                final = ''
                if a[-1] in tableData:
                    table = tableData.index(a[-1])
                    print(table)
                    colVals = sheet.col_values(table + 1)
                    lst = []
                    for i in colVals:
                        lst.append([i])
                    await message.channel.send(f'```{AsciiTable(lst).table}```')
                else:
                    await message.channel.send('bro this column doesn\'t exist, please recheck :sweat_smile:')

    if message.content.startswith(f'{prefix} show ') and '"' in message.content:
        if message.content[-1] != '"':
            a = message.content.split('"')
            if len(a) < 3:
                await message.channel.send(
                    'The command syntax is incorrect. Please use `$ts help` to check the commands.')
            else:
                try:
                    link = a[1][1:-1]
                    sheet = gClient.open_by_url(link).sheet1
                    data = sheet.findall(a[2][1:])
                    tableData = list()
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
                    await message.channel.send(
                        'Please enter a valid google sheet link. Also, if you haven\'t already, please share your google sheet with `techsyndicate@tablot-280818.iam.gserviceaccount.com`.')

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
                    await message.channel.send(
                        'Please enter a valid google sheet link. Also, if you haven\'t already, please share your google sheet with `techsyndicate@tablot-280818.iam.gserviceaccount.com`.')

            except Exception as e:
                await message.channel.send(
                    'Please enter a valid google sheet link. Also, if you haven\'t already, please share your google sheet with `techsyndicate@tablot-280818.iam.gserviceaccount.com`.')


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
            value=datetime.timedelta(seconds=difference)) \
            .set_footer(text='Made by Tech Syndicate',
                        icon_url='https://techsyndicate.co/img/logo.png')
        await message.channel.send(embed=embed)

    if message.content.startswith(f'{prefix} help'):
        embed = discord.Embed(
            title="Tablot's commands:",
            colour=1499502,
            description="""
> To use a command, type `$ts <command>`.

**General:**

`about` - To know about the bot.
`stats` - To check the bot's stats.

**Google Sheets:**

`link "<link>" variable_name` - To assign a variable to the link (only server owner)
`show variable_name` - To display the table stored in the variable
`show "<link>"` - To display the whole table
`show "<link>" value` - To display rows of specific value
""").set_footer(text='Made by Tech Syndicate', icon_url='https://techsyndicate.co/img/logo.png')
        await message.channel.send(embed=embed)

client.run(os.environ.get('TOKEN'))

# email: techsyndicate@tablot-280818.iam.gserviceaccount.com
