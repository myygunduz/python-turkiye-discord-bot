import discord
import utils


async def run(client, message, args, prefix, db):
    if len(args) == 0:
        user = message.author
        embed = discord.Embed(description=f"{user.mention} avatarı", color=utils.COLOR_EMBED)
        embed.set_image(url=user.avatar_url)

        await message.channel.send(embed = embed)

    else:
        user = utils.get_user(message.guild, args[0])
        if not user: raise Exception(f"Üye '{args[0]}' bulunamadı")

        embed = discord.Embed(description=f"{user.mention} avatarı", color=utils.COLOR_EMBED)
        embed.set_image(url=user.avatar_url)

        await message.channel.send(embed = embed)
