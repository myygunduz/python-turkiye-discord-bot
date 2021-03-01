import requests


async def run(client, message, args, prefix, db):
    if len(args) < 3:
        raise Exception("Bu komut tam olarak 3 argüman alır. Detaylar için !kullanım döviz")

    para = float(args[0])
    orj = args[1].upper()
    dvz = args[2].upper()

    res = requests.get(f"https://api.exchangeratesapi.io/latest?base={orj}").json()

    if "error" in res:
        raise Exception(f"Döviz çevrilirken bir hata oluştu, komut argümanlarını kontrol et. Detaylar için !kullanım döviz")

    if dvz not in res["rates"]:
        raise Exception(f"İstenilen kur '{dvz}' bulunamadı")

    else:
        await message.channel.send(f"💸   `{para}` {orj}  →  `{para*res['rates'][dvz]}` {dvz}")
