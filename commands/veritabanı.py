import discord
from utils import is_dev


async def run(client, message, args, prefix, db):
    if args[0] == "durum":
        await message.channel.send(f"__Veritabanı Durumu__ 🧪\n" + \
                                   f"Heroku Redis - AmazonAWS EU-West\n\n" + \
                                   f"```Bağlantı:   {('Sağlıklı', 'Ölü')[int(db.redis.connection_pool is None)]}\n" + \
                                   f"Giriş:      {int(db.elapsed*1000)}ms\n" + \
                                   f"Ort. Query: {int(db.query_elapsed*1000)}ms```" + \
                                   f"")

    elif args[0] == "kur":
        if is_dev(message.author):
            pass
        else:
            raise Exception("Bu komutu kullanmak için yeterli yetkiye sahip değilsin.")
