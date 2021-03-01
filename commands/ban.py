import utils


async def run(client, message, args, prefix, db):
    if message.author.guild_permissions.ban_members:

        if len(args) == 0:
            raise Exception("Bu komut en az bir argüman alır")

        uye = utils.get_user(message.guild, args[0])
        if not uye: raise Exception(f"Üye '{args[0]}' bulunamadı")

        try:
            await uye.ban()
            await message.channel.send(f"{uye.mention} kullanıcısı sunucudan yasaklandı.")
        except: pass

    else:
        raise Exception("Bu komutu kullanmak için gerekli yetkiye sahip değilsin")
