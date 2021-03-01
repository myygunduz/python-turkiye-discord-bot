import time
import utils


async def run(client, message, args, prefix, db):
    s = time.gmtime(time.time() - utils.LOGTIME)
    await message.channel.send(f"Bot {int(s.tm_hour)} saat, {int(s.tm_min)} dakika, {int(s.tm_sec)} saniyedir açık.")
