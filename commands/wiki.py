import discord
import utils
import wikipedia


wikipedia.set_lang("tr")
nums = ("1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣")


async def run(client, message, args, prefix, db):
    if len(args) == 0:
        raise Exception("Lütfen aramak istediğiniz anahtar kelime(leri) giriniz")

    query = " ".join(args)
    ret = wikipedia.search(query, results=6)
    if len(ret) == 0:
        raise Exception(f"'{query}' bulunamadı")
    ret.pop(0)

    if len(ret) == 1:
        ozet = wikipedia.summary(ret[0], sentences=3)

        embed = discord.Embed(title=ret[0], color=utils.COLOR_WIKI)
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/en/thumb/8/80/Wikipedia-logo-v2.svg/800px-Wikipedia-logo-v2.svg.png")
        embed.add_field(name="Açıklama", value=ozet)

        await message.channel.send(embed=embed)

    else:
        desc = "Aratmak istediğinizi seçiniz\n\n"
        for i, k in enumerate(ret):
            desc += f"{nums[i]} {k}\n"

        embed = discord.Embed(title=f"'{query}' birden fazla anlam taşıyor", description=desc, color=utils.COLOR_WIKI)
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/en/thumb/8/80/Wikipedia-logo-v2.svg/800px-Wikipedia-logo-v2.svg.png")

        m = await message.channel.send(embed=embed)
        utils.WIKI_MESAJ[m] = {"ret":ret, "user":message.author}
        for i, n in enumerate(nums):
            if i+1 > len(ret): break
            await m.add_reaction(n)
