import discord
client = discord.Client()

def about():
    embed = discord.Embed(title='Thanks for adding me to your server! :heart:',
                            description='To get started, simply share your google sheet with me at `techsyndicate@tablot-280818.iam.gserviceaccount.com`, and type `$ts help` for a list of commands.',
                            colour=1499502) \
        .add_field(
        name='Tablot',
        value='Tablot helps you conveniently display your google sheets data on a discord server.',
        inline=False).add_field(
        name='Owner',
        value='Tech Syndicate; check us out on [GitHub](https://github.com/techsyndicate).',
        inline=False
    ).set_footer(text='Made by Tech Syndicate', icon_url='https://techsyndicate.co/img/logo.png')
    
    return embed