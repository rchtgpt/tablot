import discord
import datetime

client = discord.Client()

def stats(start, current, name_list, latency, guilds):
    current_time = current
    difference = int(round(current_time - start))

    embed = discord.Embed(
        title='Statistics',
        description='',
        colour=1499502,
    ).add_field(
        name='Guild Count',
        value=len([s for s in guilds]),
        inline=True
    ).add_field(
        name='User Count',
        value=len(name_list) - 1,
        inline=True
    ).add_field(
        name='Latency',
        value=f'{latency}ms',
        inline=True
    ).add_field(
        name='Uptime',
        value=datetime.timedelta(seconds=difference)) \
        .set_footer(text='Made by Tech Syndicate',
                    icon_url='https://techsyndicate.co/img/logo.png')
    return embed