import discord
import utils
from libs import imgp


async def run(client, message, args, prefix, db):
    if len(args) == 0:
        user_dc = message.author

    else:
        user_dc = utils.get_user(message.guild, args[0])
        if not user_dc: raise Exception(f"Üye '{args[0]}' bulunamadı")

    await imgp.profil_yap(user_dc, db[user_dc], db)

    await message.channel.send(file=discord.File(f"data/profile.png"))
