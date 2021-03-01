import discord
import utils


async def run(client, message, args, prefix, db):
    embed = discord.Embed(title="Python Türkiye Discord Botu Hakkında", description="!yardım yazarak komutları görebilirsin", color=0xeb4334)
    embed.set_thumbnail(url=client.user.avatar_url)
    embed.add_field(name="__Hakkımda:__", value=f"Ben, Python Türkiye sunucusu modere etmek ve üyelere hizmet vermek amaçlı yapılmış bir botum, şikayet ve önerilerinizi yetkililere veya #öneriler kanalında belirtebilirsiniz. #bot-komut kanalında !yardım yazarak komutları inceleyebilirsiniz.", inline=False)
    embed.add_field(name="__Teknik detaylar:__", value=f"Bot versiyonu: `{utils.VERSION}`\nDiscord.py versiyonu: `{discord.__version__}`\nLisans: `MIT`\nPing: `{round(client.latency * 1000)}ms`", inline=True)
    j = client.user.created_at
    embed.add_field(name="Oluşturulma tarihi", value=f"{j.day}/{j.month}/{j.year}  {j.hour}:{j.minute}", inline=True)

    await message.channel.send(embed=embed)
