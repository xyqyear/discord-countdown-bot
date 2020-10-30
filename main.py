import discord
import shlex

from datetime import datetime

client = discord.Client()


ADMIN_CHANNEL = 'testing'
DEFAULT_MESSAGE = '{days} days till {name}'

# {'[ FAP ]:47658': {'ink_tober:36487': [['road trip', '7/1/20', 'message']]}}
countdowns = dict()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    message_content = message.content
    if message_content.startswith('/countdown '):
        args = shlex.split(message_content)[1:]
        guild_info = f'{message.guild.name}:{message.guild.id}'
        channel_info = f'{message.channel.name}:{message.channel.id}'
        # /countdown start {countdown_name} {countdown_date}
        if args[0] == 'start':
            if len(args) < 3:
                await message.channel.send(
                    'da fuq was that? you good? need some coffee? try countdown start "Name" DD/MM/YY')
                return

            # {} -> {'[ FAP ]:47658': {}}
            if guild_info not in countdowns:
                countdowns[guild_info] = dict()
            # {'[ FAP ]:47658': {}} -> {'[ FAP ]:47658': {'ink_tober:36487': []}}
            if channel_info not in countdowns[guild_info]:
                countdowns[guild_info][channel_info] = list()

            countdown_name = args[1]
            countdown_date = args[2]
            try:
                datetime.strptime(countdown_date, '%d/%m/%y')
            except ValueError:
                await message.channel.send('bruh.... you had one job! its DD/MM/YY')
                return
            # {'[ FAP ]:47658': {}} -> {'[ FAP ]:47658': {'ink_tober:36487': []}}
            # -> {'[ FAP ]:47658': {}} -> {'[ FAP ]:47658': {'ink_tober:36487': [['road trip', '7/1/20', 'message']]}}
            countdown_info = [countdown_name, countdown_date, args[3]] \
                if len(args) == 4 \
                else [countdown_name, countdown_date, DEFAULT_MESSAGE]
            print(f'new countdown added: {countdown_info}')
            countdowns[guild_info][channel_info].append(countdown_info)

        if args[0] == 'list':
            if guild_info in countdowns:
                if message.channel.name == 'testing':
                    # print all the countdowns for this guild
                    list_message = str()
                    for channel_info in countdowns[guild_info]:
                        countdown_list_str = '\n'.join(f'    {countdown[1]}: {countdown[0]}'
                                                       for countdown in countdowns[guild_info][channel_info])
                        list_message += f'\n{channel_info.split(":")[0]}:\n{countdown_list_str}'
                    list_message = list_message[1:]
                    await message.channel.send(list_message)

                else:
                    # print just the countdowns for the channel
                    if channel_info in countdowns[guild_info]:
                        countdown_list_str = '\n'.join(f'{countdown[1]}: {countdown[0]}'
                                                       for countdown in countdowns[guild_info][channel_info])
                        await message.channel.send(countdown_list_str)

client.run('NzcxNzA4OTUwNDQ5NjE4OTc0.X5wD9w.nNroDV7c6SRpUC2dRgVxysxQTA0')
