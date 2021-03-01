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

# TODO: rewrite this whole module


import discord
import os; os.environ['SDL_VIDEODRIVER'] = 'dummy'
import pygame

pygame.init()
pygame.display.set_mode((1,1))


font = pygame.font.Font("data/gil.ttf", 50)
font2 = pygame.font.Font("data/gil.ttf", 30)
circlesurf = pygame.Surface((183, 183)).convert()
circlesurf.fill((255, 0, 255))
pygame.draw.circle(circlesurf, (0, 0, 0), (91, 91), 91)
circlesurf.set_colorkey((0, 0, 0))


async def profil_yap(user, dbuser, db):
    # user -> discord.Member
    # dbuser ->
    # db -> libs.db.RedisWrapper

    if user.id == 311542309252497409: bg = pygame.image.load("data/backgrounds/sky.png")
    else: bg = pygame.Surface((650, 200), pygame.SRCALPHA).convert_alpha()
    img = pygame.Surface((650, 200), pygame.SRCALPHA).convert_alpha()

    with open("avatar.webp", "wb") as f:
        f.write(await user.avatar_url.read())

    avatar = pygame.transform.scale(pygame.image.load("avatar.webp"), (183, 183)).convert_alpha()

    avatar.set_colorkey((255, 0, 255))
    avatar.blit(circlesurf, (0, 0))
    pygame.draw.circle(avatar, (255, 0, 255), (152, 152), 29)

    name = ""
    for c in user.display_name:
        if ord(c) < 128: name += c

    ts = font.render(name, True, (255, 255, 255))
    ts2 = font.render(name, True, (0, 0, 0))
    ts3 = font2.render(f"Level {db.calc_level(dbuser)} - {dbuser-db.pre_xp(dbuser)} / {db.next_xp(dbuser)-db.pre_xp(dbuser)}", True, (255, 255, 255))
    ts4 = font2.render(f"Level {db.calc_level(dbuser)} - {dbuser-db.pre_xp(dbuser)} / {db.next_xp(dbuser)-db.pre_xp(dbuser)}", True, (0, 0, 0))
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
