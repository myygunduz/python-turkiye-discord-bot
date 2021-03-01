import discord
import utils
import time


async def run(client, message, args, prefix, db):
    userdict = {s.decode("utf-8"):int(db.redis.get(s.decode("utf-8"))) for s in db.redis.keys()}

    sortdict = sorted(userdict, key=userdict.get)

    embed = discord.Embed(color=0x609ee0)

    sunucu = client.get_guild(617712082678448158)

    for i, u in enumerate(list(reversed(sortdict))[:15]):

        xp = int(db.redis.get(u).decode("utf-8"))
        level = db.calc_level(xp)

        if i == 0:
            embed.add_field(name="឵឵", value="឵឵\n឵឵឵ ឵឵឵", inline=True)
            embed.add_field(name=f"1# {sunucu.get_member(int(u))} :first_place:", value=f"Level: `{level}` Toplam XP: `{xp}`\n឵឵឵ ឵឵឵", inline=True)
            embed.add_field(name="឵឵", value="឵឵\n឵឵឵ ឵឵឵", inline=True)
        elif i == 1:
            embed.add_field(name="឵឵", value="឵឵\n ", inline=True)
            embed.add_field(name=f"2# {sunucu.get_member(int(u))} :second_place:", value=f"Level: `{level}` Toplam XP: `{xp}`\n឵឵឵ ", inline=True)
            embed.add_field(name="឵឵", value="឵឵\n឵឵឵ ឵឵឵", inline=True)
        elif i == 2:
            embed.add_field(name="឵឵", value="឵឵\n ", inline=True)
            embed.add_field(name=f"3# {sunucu.get_member(int(u))} :third_place:", value=f"Level: `{level}` Toplam XP: `{xp}`\n឵឵឵ ", inline=True)
            embed.add_field(name="឵឵", value="឵឵\n឵឵឵ ឵឵឵", inline=True)
        else:
            embed.add_field(name=f"{i+1}# {sunucu.get_member(int(u))}", value=f"Level: `{level}` Toplam XP: `{xp}`\n឵឵឵ ", inline=True)

    await message.channel.send(embed=embed)

    utils.SON_top15 = time.time()
