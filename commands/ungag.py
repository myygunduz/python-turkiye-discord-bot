import utils


async def run(client, message, args, prefix, db):
    if message.author.guild_permissions.manage_messages:
        gag = message.guild.get_role(751514494307663949)
        uye = utils.get_user(message.guild, args[0])
        if not uye: raise Exception(f"Üye '{args[0]}' bulunamadı")

        try:
            await uye.remove_roles(gag)
            await message.channel.send(f"{uye.mention} kullanıcısı üzerinden süresiz chat yasağı kaldırıldı")
        except: pass

    else:
        raise Exception("Bu komutu kullanmak için gerekli yetkiye sahip değilsin")
