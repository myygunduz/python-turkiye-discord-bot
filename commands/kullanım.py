import discord
import utils


async def run(client, message, args, prefix, db):
    if args[0] in utils.KOMUTLAR:
        if args[0] == "döviz":
            embed = discord.Embed(title=f"{prefix}{args[0]} kullanımı", description="Girilen parayı güncel döviz kuruna göre çevirir", color=0x598096)
            embed.add_field(name="Syntax", value=f"!döviz `para: (int, float)` `orjinal: str` `döviz: str`\n- **para**: Çevrilmek istenen miktar\n- **orjinal**: Paranın hangi kura ait olduğu\n- **döviz**: Paranın hangi kura çevrileceği", inline=False)
            embed.add_field(name="Örnekler", value=f"!döviz 20 try usd\n!döviz 142.4 try usd", inline=False)
            await message.channel.send(embed=embed)

    else:
        raise Exception(f"{prefix}{args[0]} diye bir komut bulunmuyor")
