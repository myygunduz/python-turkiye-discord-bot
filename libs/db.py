# Part of the Python Türkiye Discord Bot's libraries
#
# EN:
# Uses Redis database to store user levels. Change
# os.environ["REDIS_URL"] with your own redis server
# address if you are using this project as skeleton for your bot.
#
# TR:
# Üyelerin seviyelerini saklamak için Redis veritabanı
# kullanır. Eğer bu projeyi kendi botunuz için bir
# temel olark kullanıyorsanız os.environ["REDIS_URL"] kısmını
# kendi redis sunucu adresiniz ile değiştirin.
#
# https://github.com/kadir014/python-turkiye-discord-bot


from urllib.parse import urlparse
import os
import time
import redis

url = urlparse(os.environ["REDIS_URL"])


class RedisWrapper:
    def __init__(self):
        self.level_sheet = (0, 50, 200, 700, 5700, 20700, 70700)
        s = time.time()
        self.redis = redis.Redis(host=url.hostname, port=url.port, username=url.username, password=url.password, ssl=False, ssl_cert_reqs=None)
        self.elapsed = time.time() - s
        self.queries = list()
        self.query_elapsed = 0

    def __getitem__(self, s):
        ss = time.time()

        if self.redis.exists(str(s.id)):
            r = int(self.redis.get(str(s.id)))
            self.queries.append(time.time()-ss)
            self.calc_avg_query()
            return r
        else:
            self.__setitem__(s, 1)
            self.queries.append(time.time()-ss)
            self.calc_avg_query()
            return 1

    def __setitem__(self, s, v):
        ss = time.time()

        self.redis.set(str(s.id), v)

        self.queries.append(time.time()-ss)
        self.calc_avg_query()

    def new_user(self, user):
        s = time.time()

        self.redis.set(str(user.id), 1)

        self.queries.append(time.time()-s)
        self.calc_avg_query()

    def remove_user(self, user):
        s = time.time()

        self.redis.delete(str(user.id))

        self.queries.append(time.time()-s)
        self.calc_avg_query()

    def calc_avg_query(self):
        if len(self.queries) > 30: self.queries.pop(0)
        self.query_elapsed = sum(self.queries) / len(self.queries)

    # XP -> Level çevirme

    def calc_level(self, xp):
        level = 0
        for i in self.level_sheet:
            if xp >= i: level += 1

        return level

    def pre_xp(self, xp):
        for i, level in enumerate(self.level_sheet[::-1]):
            if xp == level:
                if i == 0: return 0
                return self.level_sheet[i-1]

            elif xp > level:
                return level

    def next_xp(self, xp):
        for i, level in enumerate(self.level_sheet):
            if xp == level:
                if i == 6: return level
                return self.level_sheet[i+1]

            elif xp < level:
                return level
