
from libs.jsonHelper import writeJ, readJ

async def run(client, message, args, prefix, db):
    pollsDict = readJ('data/polls.json')
    settings = {
        'message':'',
        'author':message.author.id,
        'emojis':[],
        'emojiWaitMessage':''
    }
    await client.send("Anket mesajını girin:")

    def waitMessage(m):
        if m.channel == message.channel and m.author.id == client.author.id:
            return m

    msg = await client.wait_for("message", check=waitMessage, timeout=30)

    settings['message'] = msg.content

    waitEmoji = await message.send("Emojileri sırayla belirtin. (Bu mesajın altına. Bittiğinde herhangi birşey yazın.)")
    settings['emojiWaitMessage'] = waitEmoji.content

    pollsDict['formed'].append(settings)
    writeJ(pollsDict,'data/polls.json')


    def waitMessageForClose(m):
        if m.channel == message.message.channel and m.author.id == message.author.id:
            return m

    finish = await client.wait_for("message", check=waitMessageForClose, timeout=50)
    pollsDict = readJ('data/polls.json')

    channel = client.get_guild(873283861352706080) #burayı değiştir anket kanalının idsi yap
    for i in pollsDict['formed']:
        if i['author'] == message.author.id:
            message = await channel.send(i['message']+f"\n||```Anketi Oluşturanın Bilgileri:\nid:{message.author.id}\nİsmi:{message.author.name}```||")
            for emoji in i['emojis']:
                await message.add_reaction(emoji)
            pollsDict['formed'].pop(pollsDict['formed'].index(i))

    writeJ(pollsDict,'data/polls.json')