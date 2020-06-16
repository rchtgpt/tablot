import discord
import os
from dotenv import load_dotenv
from terminaltables import AsciiTable
import gspread
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()
#TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

# table data
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
gClient = gspread.authorize(creds)

@client.event
async def on_ready():
    print('i\'m ready to get back to work')

@client.event
async def on_message(message):

    if message.content.startswith(f'!ts show "'):
        if message.content[-1] != '"':
            await message.channel.send('bhai naam toh dhang se likh le')
        else:
            try:
                a = message.content.split('"')
                sheet = gClient.open(a[1]).sheet1
                data = sheet.get_all_records()

                tableData = [[key for key in data[0].keys()]]
                for i in data:
                    val = [value for value in i.values()]
                    tableData.append(val)

                table = AsciiTable(tableData)
                await message.channel.send(f'```{table.table}```')
            except:
                await message.channel.send('pls junos dis is incorrect file name')
    if message.content.startswith('!ts github'):
        await message.channel.send('Star our github repo at https://github.com/techsyndicate/tablot     :smiling_face_with_3_hearts:')
client.run('NzIyMzM5MjcwODE5NDQ2ODM1.XuhrsA.G84dyI2FlrhPXKPK7bxdywKc84c')
#isko hatana while pushing

# web scraping - future?
# email: mihir-462@tablot-280404.iam.gserviceaccount.com

'''
Commands: 
1. $ts about - bot introduces itself ($hello --> $about)
2. $ts ping - check the bot's latency (j)
3. $ts github - display github repo (j)
4. $ts stats - as the name suggests 
4. ts show "file name"

6. $ts sheet name rachit
serial number: 1
name: Rachit
class: XI - C
stream: science
'''


