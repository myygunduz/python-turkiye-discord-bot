async def run(client, message, args, prefix, db):
    if message.author.guild_permissions.manage_messages:

        if len(args) > 0:

            if args[0].isdigit():
                msgs = list()
                async for msg in message.channel.history(limit = int(args[0])+1):
                    msgs.append(msg)

                await message.channel.delete_messages(msgs)

            else:
                raise Exception("!temizle komudu argüman olarak sayı alır")

        else:
            raise Exception("!temizle komudu en az bir argüman gerektirir")

    else:
        raise Exception("Bu komutu kullanmak için gerekli yetkiye sahip değilsin")
