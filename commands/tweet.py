import discord
import utils
import ast
from libs import imgp
import pygame


async def run(client, message, args, prefix, db):
    if len(args) == 0:
        user_dc = message.author

    else:
        user_dc = utils.get_user(message.guild, args[0])
        if not user_dc: raise Exception(f"Üye '{args[0]}' bulunamadı")

    pargs = ast.literal_eval(" ".join(args[1:]))
    if not "tname" in pargs: pargs["tname"] = ""
    if not "date" in pargs: pargs["date"] = ""
    if not "rt" in pargs: pargs["rt"] = 0
    if not "love" in pargs: pargs["love"] = 0

    a = await imgp.generate_tweet(user_dc, pargs["text"], pargs["tname"], pargs["date"], pargs["rt"], pargs["love"])
    pygame.image.save(a, "data/tweet.png")

    await message.channel.send(file=discord.File(f"data/tweet.png"))
