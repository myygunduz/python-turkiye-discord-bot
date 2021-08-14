import utils
async def run(client, message, args, prefix, db):

    def waitMessage(m):
        if m.channel == message.channel and m.author.id == client.author.id:
            return m

    def sendMessage(channel,m):
        await channel.send(m)

    settings = {
        'message':'',
        'author':message.author.id,
        'emojis':[],
        'emojiWaitMessage':''}

    sendMessage(client,"Anket mesajını girin:")

    msg = await client.wait_for("message", check=waitMessage, timeout=30)


    waitEmoji = await message.send("Emojileri sırayla belirtin. (Bu mesajın altına. Bittiğinde herhangi birşey yazın.)")
    
    settings['message'] = msg.content
    settings['emojiWaitMessage'] = waitEmoji.content

    utils.POOLSDICT.append(settings)

    finish = await client.wait_for("message", check=waitMessage, timeout=50)

    channel = client.get_guild(873283861352706080) #burayı değiştir anket kanalının idsi yap
    for i in utils.POOLSDICT:
        if i['author'] == message.author.id:
            message = await channel.send(i['message']+f"\n||```Anketi Oluşturanın Bilgileri:\nid:{message.author.id}\nİsmi:{message.author.name}```||")
            for emoji in i['emojis']:
                await message.add_reaction(emoji)
            utils.POOLSDICT.pop(utils.POOLSDICT.index(i))