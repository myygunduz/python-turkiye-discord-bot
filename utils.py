import discord
import time


VERSION = "0.1.3"

POSITIVE = "<:positive:715519331655483462>"
NEGATIVE = "<:negative:715519331768729684>"
UPVOTE   = "<:upvote:715196324512792620>"
DOWNVOTE = "<:downvote:715196362362454016>"

COLOR_DEFAULT = 0x8a4cfc
COLOR_EMBED   = 0x2f3136
COLOR_ERROR   = 0xf44336
COLOR_WARN    = 0xffd045
COLOR_COVID   = 0x4caf4f
COLOR_WIKI    = 0xe6ecf2

LOGTIME = 0
SON_SAYI = 0
SON_MESAJLAR = {}
# !top15 komutu kaynakları çok kullandığı için her 3 dakikada bir kullanılabilir
SON_top15 = 0

WIKI_MESAJ = {}

KOMUTLAR = []

LEVEL1 = None
LEVEL2 = None
LEVEL3 = None
LEVEL4 = None
LEVEL5 = None
LEVEL6 = None
LEVEL7 = None

POOLSDICT = {}


def update_levels(guild):
    global LEVEL1, LEVEL2, LEVEL3, LEVEL4, LEVEL5, LEVEL6, LEVEL7
    LEVEL1 = guild.get_role(731954451782565900)
    LEVEL2 = guild.get_role(733660568551948288)
    LEVEL3 = guild.get_role(733660682058203247)
    LEVEL4 = guild.get_role(733660690103140373)
    LEVEL5 = guild.get_role(733660688148463627)
    LEVEL6 = guild.get_role(733660686529331310)
    LEVEL7 = guild.get_role(733661298323226784)

async def update_level_role(member, level):
    for role in member.roles:
        if LEVEL1 == role: await member.remove_roles(LEVEL1); break
        if LEVEL2 == role: await member.remove_roles(LEVEL2); break
        if LEVEL3 == role: await member.remove_roles(LEVEL3); break
        if LEVEL4 == role: await member.remove_roles(LEVEL4); break
        if LEVEL5 == role: await member.remove_roles(LEVEL5); break
        if LEVEL6 == role: await member.remove_roles(LEVEL6); break
        if LEVEL7 == role: await member.remove_roles(LEVEL7); break

    if   level == 1: await member.add_roles(LEVEL1)
    elif level == 2: await member.add_roles(LEVEL2)
    elif level == 3: await member.add_roles(LEVEL3)
    elif level == 4: await member.add_roles(LEVEL4)
    elif level == 5: await member.add_roles(LEVEL5)
    elif level == 6: await member.add_roles(LEVEL6)
    elif level == 7: await member.add_roles(LEVEL7)

def calctime(func, *args, **kwargs):
    s = time.time()
    r = func(*args, **kwargs)
    return time.time()-s, r

def get_user(guild, arg):
    # guild -> discord.Guild
    # arg   -> user mention string
    # arg   -> user ID
    # arg   -> username / username#discriminator

    if isinstance(arg, discord.User) or isinstance(arg, discord.Member):
        return arg

    else:
        if arg.startswith("<@!") or arg.startswith("<@"):
            s = ""
            for char in str(arg):
                if char.isdigit(): s += char

            user = guild.get_member(int(s))
            if user: return user

        try:
            user = guild.get_member(int(arg))
            if user: return user

        except:
            argl = arg.lower()
            for member in guild.members:
                if member.name.lower() == argl or str(member).lower() == argl or argl in member.name.lower() or member.display_name.lower() == argl or argl in member.display_name.lower():
                    return member

                if member.nick:
                    if member.nick.lower() == argl or argl in member.nick.lower():
                        return member

def is_dev(user):
    # user -> discord.User

    if user.id in (311542309252497409,):
        return True

async def feed_error(exception, client, message, args, prefix):
    await message.channel.send(f"Komut çalıştırılırken bir hata meydana geldi: `{exception}`")
    cmd = message.content[len(prefix):message.content.find(" ")+1]
    print(f"Hata: {str(message.author)} > {prefix}{cmd} {' '.join(args)} => {exception}")
    embed = discord.Embed()
