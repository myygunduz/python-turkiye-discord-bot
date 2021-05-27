# Part of the Python Türkiye Discord Bot's libraries
#
# EN:
# Uses pygame to create image that displays user's level.
#
# TR:
# Kullanıcıların seviyelerini gösteren görseli
# oluşturmak için pygame kullanır.
#
# https://github.com/kadir014/python-turkiye-discord-bot


import os; os.environ['SDL_VIDEODRIVER'] = 'dummy'
import discord
import pygame
import datetime

pygame.init()
pygame.display.set_mode((1,1))


tweet_follow = pygame.image.load("data/tweet_follow.png").convert()
tweet_controls = pygame.image.load("data/tweet_controls.png").convert()

fonts = {
    "Segoe UI - 24" : pygame.font.Font("data/Segoe UI.ttf", 24),
    "Gil - 30" : pygame.font.Font("data/gil.ttf", 30),
    "Gil - 50" : pygame.font.Font("data/gil.ttf", 50)
}

turkish_chars = {"ç":"c", "ğ":"g", "ı":"i", "ö":"o", "ü":"u",
                 "Ç":"C", "Ğ":"G", "İ":"I", "Ö":"O", "Ü":"U"}

# TODO: Optimize
def circle_mask(surface):
    circlesurf = pygame.Surface(surface.get_size()).convert()
    circlesurf.fill((255, 0, 254))
    c = surface.get_width()/2
    pygame.draw.circle(circlesurf, (0, 0, 0), (c, c), c)
    circlesurf.set_colorkey((0, 0, 0))

    resultsurf = pygame.Surface(surface.get_size())
    resultsurf.set_colorkey((255, 0, 254, 255))
    resultsurf.blit(surface, (0, 0))
    resultsurf.blit(circlesurf, (0, 0))

    returnsurf = pygame.Surface(surface.get_size(), pygame.SRCALPHA).convert_alpha()
    returnsurf.blit(resultsurf, (0, 0))

    return returnsurf


async def get_avatar(user):
    with open("data/_tempavatar.webp", "wb") as f: f.write(await user.avatar_url.read())

    return pygame.image.load("data/_tempavatar.webp").convert_alpha()


async def generate_tweet(user, textt, tname="", date="", rt=0, love=0):
    # user -> discord.Member

    s = ""
    for char in textt:
        if char in turkish_chars: s += turkish_chars[char]
        else: s += char
    text = s
    name = user.display_name
    if len(tname) == 0: tname = name.lower().replace(" ", "_").replace("-", "_")
    if len(date) == 0: date = datetime.datetime.now().strftime("%H:%M - %d %m %Y")

    if rt > 10000: rt = f"{int(rt/1000)}K"
    elif rt > 1000: rt = str(rt)[0] + "," + str(rt)[1:]

    if love > 10000: love = f"{int(love/1000)}K"
    elif love > 1000: love = str(love)[0] + "," + str(love)[1:]

    surface = pygame.Surface((700, 307)).convert()
    surface.fill((255, 255, 255))

    avatar = await get_avatar(user)
    avatar = pygame.transform.scale(avatar, (55, 55)).convert_alpha()

    surface.blit(avatar, (30, 30))
    surface.blit(tweet_follow, (535, 30))
    surface.blit(tweet_controls, (33, 258))

    surface.blit(fonts["Segoe UI - 24"].render(name,        True, (28, 32, 35)),    (100, 26))
    surface.blit(fonts["Segoe UI - 24"].render(f"@{tname}", True, (110, 125, 140)), (100, 55))
    surface.blit(fonts["Segoe UI - 24"].render(date,        True, (110, 125, 140)), (30, 210))
    surface.blit(fonts["Segoe UI - 24"].render(str(rt),     True, (100, 120, 130)), (123, 255))
    surface.blit(fonts["Segoe UI - 24"].render(str(love),   True, (100, 120, 130)), (233, 255))

    lines = []
    words = text.split(" ")
    print(len(words))
    w = 0
    s = ""
    for word in words:
        w += len(word) + 1
        s += word + " "
        if w > 46:
            lines.append(s)
            s = ""
            w = 0

    if len(lines) == 0: lines.append(word)

    lines = lines[:3]

    for y, line in enumerate(lines):
        surface.blit(fonts["Segoe UI - 24"].render(line, True, (28, 32, 35)), (30, 100+(y*26)))

    return surface


async def profil_yap(user, dbuser, db):
    # user -> discord.Member
    # dbuser ->
    # db -> libs.db.RedisWrapper

    if   user.id == 311542309252497409: bg = pygame.image.load("data/backgrounds/sky.png")
    elif user.id == 365120946299731990: bg = pygame.image.load("data/backgrounds/reis.png")
    else: bg = pygame.Surface((650, 200), pygame.SRCALPHA).convert_alpha()
    img = pygame.Surface((650, 200), pygame.SRCALPHA).convert_alpha()

    avatar = await get_avatar(user)
    avatar = pygame.transform.scale(avatar, (183, 183)).convert_alpha()

    avatar = circle_mask(avatar)
    avatar.set_colorkey((255, 0, 254))
    pygame.draw.circle(avatar, (255, 0, 254), (152, 152), 29)

    name = ""
    for c in user.display_name:
        if c in turkish_chars: name += turkish_chars[c]
        elif ord(c) < 128: name += c

    ts = fonts["Gil - 50"].render(name, True, (255, 255, 255))
    ts2 = fonts["Gil - 50"].render(name, True, (0, 0, 0))
    ts3 = fonts["Gil - 30"].render(f"Level {db.calc_level(dbuser)} - {dbuser-db.pre_xp(dbuser)} / {db.next_xp(dbuser)-db.pre_xp(dbuser)}", True, (255, 255, 255))
    ts4 = fonts["Gil - 30"].render(f"Level {db.calc_level(dbuser)} - {dbuser-db.pre_xp(dbuser)} / {db.next_xp(dbuser)-db.pre_xp(dbuser)}", True, (0, 0, 0))
    outline = pygame.Surface((650, 200), pygame.SRCALPHA).convert_alpha()
    pygame.draw.circle(outline, (255, 255, 255), (99, 99), 93)
    pygame.draw.circle(outline, (255, 0, 255), (152, 152), 29)
    outline.set_colorkey((255, 0, 255))
    img.blit(outline, (0, 0))

    if user.status == discord.Status.online:
        status = pygame.image.load("data/status/cevrimici.png")
    elif user.status == discord.Status.dnd:
        status = pygame.image.load("data/status/rahatsiz.png")
    elif user.status == discord.Status.idle:
        status = pygame.image.load("data/status/bosta.png")
    else:
        status = pygame.image.load("data/status/cevrimdisi.png")

    img.blit(status, (0, 0))

    bar = pygame.Surface((650, 200), pygame.SRCALPHA).convert_alpha()
    bar.fill((255, 0, 255, 255))
    bar.set_colorkey((255, 0, 255))
    pygame.draw.rect(bar, (0, 0, 0, 190), (178, 72, 617-178, 125-72))
    pygame.draw.circle(bar, (0, 0, 0, 190), (617, 99), (125-72)/2)

    xp_orani = (dbuser-db.pre_xp(dbuser)) / (db.next_xp(dbuser)-db.pre_xp(dbuser))
    pygame.draw.rect(bar, (0, 255, 0, 220), (178, 72, (617-178)*xp_orani, 125-72))
    pygame.draw.circle(bar, (0, 255, 0, 220), (178+(617-178)*xp_orani, 99), (125-72)/2)

    pygame.draw.circle(bar, (255, 0, 255, 255), (113, 99), 91)

    img.blit(bar, (0, 0))
    img.blit(avatar, (8, 8))
    img.blit(ts2, (197, 14))
    img.blit(ts2, (198, 10))
    img.blit(ts2, (196, 10))
    img.blit(ts2, (198, 14))
    img.blit(ts2, (196, 14))
    img.blit(ts, (197, 10))
    img.blit(ts4, (200, 142))
    img.blit(ts4, (201, 140))
    img.blit(ts4, (199, 140))
    img.blit(ts4, (201, 142))
    img.blit(ts4, (199, 142))
    img.blit(ts3, (200, 140))

    if user.id == 311542309252497409: img.blit(pygame.image.load("data/badges/satania.png"), (0, 0))

    bg.blit(img, (0, 0))

    pygame.image.save(bg, "data/profile.png")
