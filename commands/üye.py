import discord
import utils


async def run(client, message, args, prefix, db):
    if len(args) == 0:
        user = message.author
    else:
        user = utils.get_user(message.guild, args[0])
        if not user: raise Exception(f"Üye '{args[0]}' bulunamadı")

    embed = discord.Embed(title=f"**{user.name}** hakkında", color=0x6675ff)
    embed.set_footer(text=f"Bu havalı kullanıcının ID'si {user.id}")
    embed.set_thumbnail(url=user.avatar_url)
    j = user.joined_at
    embed.add_field(name="Sunucuya katılma tarihi", value=f"{j.day}/{j.month}/{j.year}  {j.hour}:{j.minute}", inline=True)
    j = user.created_at
    embed.add_field(name="Hesabını açma tarihi", value=f"{j.day}/{j.month}/{j.year}  {j.hour}:{j.minute}", inline=True)
    roles = user.roles
    for r in roles:
        if r.id == 731954285595590678 or r.id == 712996348181610561 or r.id == 712996541119332455:
            roles.remove(r)

    if len(roles) == 1:
        roles = "Bu kişinin hiç rolü yok"
    else:
        roles = [r.mention for r in roles]
        roles.pop(0)
        roles = " ".join(roles)
    embed.add_field(name="Roller", value=roles, inline=False)

    await message.channel.send(embed=embed)
