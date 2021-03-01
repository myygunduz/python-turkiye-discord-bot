import discord
import utils
from libs import covidapi


async def run(client, message, args, prefix, db):
    if len(args) == 0: arg = "global"
    else: arg = " ".join(args)

    if arg == "uk": arg = "united kingdom"
    elif arg == "usa": arg = "us"

    j = covidapi.get_key(covidapi.updater.summary, arg)

    if arg == "global": title = f"COVID-19 küresel durumu"
    else: title = f"{j['Country']} COVID-19 durumu"

    embed = discord.Embed(title=title, color=utils.COLOR_COVID)
    embed.set_thumbnail(url="https://i.imgur.com/ZHNq1fi.png")
    embed.add_field(name="__Vaka__", value=f"Yeni: `{j['NewConfirmed']}`\nToplam: `{j['TotalConfirmed']}`", inline=True)
    embed.add_field(name="__Ölüm__", value=f"Yeni: `{j['NewDeaths']}`\nToplam: `{j['TotalDeaths']}`", inline=True)
    embed.add_field(name="__İyileşen__", value=f"Yeni: `{j['NewRecovered']}`\nToplam: `{j['TotalRecovered']}`", inline=True)
    if "Date" in j: embed.set_footer(text=f"En son {j['Date']} tarihinde güncellendi")

    await message.channel.send(embed=embed)
