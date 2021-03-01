import discord


async def run(client, message, args, prefix, db):
    embed = discord.Embed(title="Python Türkiye Sunucu Bilgisi", description=f"Bu sunucunun sahibi {message.guild.owner.mention}", color=0xeb4334)
    embed.set_footer(text=f"Sunucu ID'si {message.guild.id}")
    embed.set_thumbnail(url=message.guild.icon_url)

    members = message.guild.members
    online = 0
    offline = 0
    bot = 0
    dnd = 0
    idle = 0

    for m in members:
        if m.bot: bot += 1
        elif m.status == discord.Status.online: online += 1
        elif m.status == discord.Status.offline or m.status == discord.Status.invisible: offline += 1
        elif m.status == discord.Status.idle: idle += 1
        elif m.status == discord.Status.dnd: dnd += 1

    embed.add_field(name=f"__{bot+online+idle+dnd}/**{message.guild.member_count}** Üye__", value=f":green_circle: **{online}** Online\n:orange_circle: **{idle}** Boşta\n:red_circle: **{dnd}** Meşgul\n:white_circle: **{offline}** Çevrimdışı\n:robot: **{bot}** Bot")
    embed.add_field(name=f"__**{len(message.guild.channels)}** Kanal__", value=f"Metin: **{len(message.guild.text_channels)}**\nSesli: **{len(message.guild.voice_channels)}**\nKategoriler: **{len(message.guild.categories)}**")
    j = message.guild.created_at
    embed.add_field(name="__Oluşturulma tarihi__", value=f"{j.day}/{j.month}/{j.year}  {j.hour}:{j.minute}")

    await message.channel.send(embed=embed)
