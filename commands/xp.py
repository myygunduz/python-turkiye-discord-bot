from utils import is_dev, get_user


async def run(client, message, args, prefix, db):
    if is_dev(message.author):
        user = get_user(message.guild, args[0])
        if not user:
            raise Exception(f"'{args[0]}' bulunamadı")

        if args[1].startswith("+"):
            db[user] = db[user] + int(args[1][1:])

        elif args[1].startswith("-"):
            db[user] = db[user] + int(args[1][1:])

        else:
            db[user] = int(args[1])

    else:
        raise Exception("Bu komutu kullanabilmek için yeterli yetkiye sahip değilsiniz")
