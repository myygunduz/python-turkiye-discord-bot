import discord


async def run(client, message, args, prefix, db):
    if message.author.id in (311542309252497409, 300191414569009153):
        if len(message.channel_mentions) == 0:
            chn = message.channel
            msg = " ".join(args)
        else:
            chn = message.channel_mentions[0]
            msg = " ".join(args[1:])

        await message.delete()
        embed = discord.Embed.from_dict(eval(" ".join(args[1:])))
        embed.set_thumbnail(url=message.guild.icon_url)
        await chn.send(embed=embed)
