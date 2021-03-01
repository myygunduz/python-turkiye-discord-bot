async def run(client, message, args, prefix, db):
    r = "".join(open('data/yardım.txt', 'r', encoding="utf-8").readlines())
    await message.channel.send("```diff\n" + r + "\n```")
