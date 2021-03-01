#               Python Türkiye Discord Botu
#                   Kadir Aksoy - 2020
# https://github.com/kadir014/python-turkiye-discord-bot


import os
import time
import discord
import utils
from libs.db import RedisWrapper
from libs import covidapi
import wikipedia


db = RedisWrapper()

intents = discord.Intents.all()
client = discord.Client(intents=intents)

prefix = "!"


############################################
#                                          #
#               EVENT İŞLEME               #
#                                          #
############################################


@client.event
async def on_ready():
    await client.change_presence(activity = discord.Game(name=f"!yardım"))

    sunucu = client.get_guild(617712082678448158)
    utils.update_levels(sunucu)

    # Sayı sayma oyununda son sayıyı yenile
    async for message in sunucu.get_channel(791005443833069569).history(limit=1):
        utils.SON_SAYI = int(message.content)

    print("\nBot başarıyla giriş yaptı\n_________________________________\n")

@client.event
async def on_member_join(member):
    print(f"Kullanıcı giriş yaptı: {member.name}")
    db.new_user(member)

    r1 = member.guild.get_role(712997327513845822)
    r4 = member.guild.get_role(731954285595590678)
    r5 = member.guild.get_role(731954451782565900)
    try: await member.add_roles(r1)
    except: pass
    try: await member.add_roles(r4)
    except: pass
    try: await member.add_roles(r5)
    except: pass

@client.event
async def on_member_remove(member):
    print(f"Kullanıcı çıkış yaptı: {member.name}")
    db.remove_user(member)

@client.event
async def on_reaction_add(reaction, user):
    if user.bot: return

    # Wikipedia mesajına verilen reaction
    if reaction.message in utils.WIKI_MESAJ:
        if user != utils.WIKI_MESAJ[reaction.message]["user"]: return
        ret = utils.WIKI_MESAJ[reaction.message]["ret"]
        utils.WIKI_MESAJ.pop(reaction.message)

        if reaction.emoji   == "1️⃣": num = 0
        elif reaction.emoji == "2️⃣": num = 1
        elif reaction.emoji == "3️⃣": num = 2
        elif reaction.emoji == "4️⃣": num = 3
        elif reaction.emoji == "5️⃣": num = 4

        wikipedia.set_lang("tr")
        ozet = wikipedia.summary(ret[num], sentences=3)

        embed = discord.Embed(title=ret[num], color=utils.COLOR_WIKI)
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/en/thumb/8/80/Wikipedia-logo-v2.svg/800px-Wikipedia-logo-v2.svg.png")
        embed.add_field(name="Açıklama", value=ozet)

        try:
            await reaction.message.channel.send(embed=embed)
            await reaction.message.delete()
        except: pass


############################################
#                                          #
#               KOMUT İŞLEME               #
#                                          #
############################################


# Bu komutlar yazıldığı gibi silineceği için try/except bloğuna girmemeliler
pass_cmds = ("say", "embed", "temizle")

for (dirpath, dirnames, filenames) in os.walk("./commands"):
    for filename in filenames:
        if not filename[-3:] == '.py': continue
        utils.KOMUTLAR.append(filename[:-3])

print("Yüklenen komutlar:")
for cmd in utils.KOMUTLAR:
    print(f"  {cmd}")


@client.event
async def on_message(message):
    if message.author.bot: return
    elif isinstance(message.channel, discord.channel.DMChannel): return

    if message.content.startswith(prefix):
        cmd, args = message.content.split(" ")[0][len(prefix):], message.content.split(" ")[1:]

        if cmd in utils.KOMUTLAR:
            # top15 komutu çok kaynak yediği için cooldown getirildi
            if cmd == "top15":
                if time.time() - utils.SON_top15 < 180:
                    await message.channel.send("Bu komut her 3 dakikada bir kullanılabilir")
                    await message.add_reaction(utils.NEGATIVE)
                else:
                    cmdfile = __import__(f"commands.top15", fromlist=["top15",])
                    await cmdfile.run(client, message, args, prefix, db)
                    await message.add_reaction(utils.POSITIVE)

            else:
                cmdfile = __import__(f"commands.{cmd}", fromlist=[cmd])

                try:
                    await cmdfile.run(client, message, args, prefix, db)
                    if cmd in pass_cmds: return
                    await message.add_reaction(utils.POSITIVE)

                except Exception as e:
                    await utils.feed_error(e, client, message, args, prefix)
                    if cmd in pass_cmds: return
                    await message.add_reaction(utils.NEGATIVE)

        # DEBUGGING

        elif cmd == "ping":
            await message.channel.send(f"Pong! `{client.latency}`ms")

        elif cmd == "debug":
            if args[0] == "get_user":
                dt, user = utils.calctime(utils.get_user, message.guild, args[1])
                if user: await message.channel.send(f"`get_user` düzgün çalışıyor\nExecute time: {int(dt*1000)}ms\n@return -> discord.User({user.name}#{user.discriminator})")
                else: await message.channel.send(f"`get_user` düzgün çalışıyor\nExecute time: {int(dt*1000)}ms\n@return -> None")

            elif args[0] == "redis_all":
                sunucu = client.get_guild(617712082678448158)
                userdict = {sunucu.get_member(int(s.decode("utf-8"))).name:int(db.redis.get(s.decode("utf-8"))) for s in db.redis.keys()}
                await message.channel.send(f"{userdict}")

    else:
        # SAYI SAYMA OYUNU
        if message.channel.id == 791005443833069569:
            if message.content.isdigit():
                if int(message.content) == utils.SON_SAYI + 1:
                    utils.SON_SAYI = int(message.content)

                else:
                    try: await message.author.send(f"Sayı sayma oyununda girmeniz gereken sayı `{utils.SON_SAYI + 1}` iken siz `{int(message.content)}` girdiniz.")
                    except: pass
                    await message.delete()
                    return
            else:
                try: await message.author.send(f"Lütfen sayı sayma oyununda sayı kullanınız.")
                except: pass
                await message.delete()
                return

        # KELİME TÜRETMECE OYUNU
        elif message.channel.id == 791005667056943105:
            pass

        # ÖNERİ
        elif message.channel.id == 710483917349584963:
            await message.add_reaction(utils.UPVOTE)
            await message.add_reaction(utils.DOWNVOTE)

        # PROJE PAYLAŞIM
        elif message.channel.id == 784725540157521930:
            await message.add_reaction("⭐")

        # NORMAL MESAJ
        else:
            # En son attığı mesajın üzerinden 5 saniye geçmeli
            if not (message.author.id in utils.SON_MESAJLAR): utils.SON_MESAJLAR[message.author.id] = time.time()
            if time.time() - utils.SON_MESAJLAR[message.author.id] < 5: return

            # Atılan mesajın kaç XP getireceğini hesapla
            inc = len(message.content.replace(" ", "")) / 20
            if inc <= 1: inc = 1
            else: inc = int(inc)

            # Mesajın atıldığı yere göre XP'yi çoğalt
            if message.channel.id in (714812174668922931, 784725540157521930):
                inc *= 3

            db[message.author] = db[message.author] + inc

            xp = db[message.author]

            if db.calc_level(xp) != db.calc_level(xp-inc):
                await utils.update_level_role(message.author, db.calc_level(xp))

            utils.SON_MESAJLAR[message.author.id] = time.time()


utils.LOGTIME = time.time()
client.run(os.environ["TOKEN"])
