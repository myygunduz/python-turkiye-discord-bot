import utils


async def run(client, message, args, prefix, db):
    if utils.is_dev(message.author):
        mesaj = message.content[len(prefix) + len("duyuru"):]
        basarisiz = list()

        for i, u in enumerate(message.guild.members):
            if not u.bot:
                try:
                    if u.id == 466306304063832065: continue
                    if u.id == 302515395552739339: continue
                    if u.id == 284697871331360778: continue
                    dm = await u.create_dm()
                    await dm.send(mesaj.format(u.name))

                except Exception as e:
                    print(message.author.display_name + " : " + message.content + " >>")
                    print(e)
                    basarisiz.append(u)

            print(f"Duyuru {i}/{len(message.guild.members)}")

        if len(basarisiz) != 0:
            basarisiz_string = ""
            for u in basarisiz:
                basarisiz_string = basarisiz_string + str(u) + " \n"
            await message.channel.send("Duyuruyu almayan kişiler:\n```" + basarisiz_string + "```")

            for b in basarisiz:
                print(str(b.name), b.name, b.id)
    else:
        raise Exception("Bu komutu kullanmak için yeterli yetkiye sahip değilsin.")
