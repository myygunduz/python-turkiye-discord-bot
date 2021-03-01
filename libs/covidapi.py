# Part of the Python Türkiye Discord Bot's libraries
#
# EN:
# Uses covid19api.com to retrieve and store latest
# coronavirus information. Updater thread updates
# the status ever 28 minutes.
#
# TR:
# En son koronavirüs bilgisini almak ve saklamak için
# covid19api.com'u kullanır. Updater thread'i durumu
# her 28 dakikada bir günceller.
#
# https://github.com/kadir014/python-turkiye-discord-bot


import requests
import threading
import time


class CountryNotFound(Exception): pass

BASE_URL = "https://api.covid19api.com/summary"


def get_all():
    return requests.get(BASE_URL).json()

def get_key(data, key):
    if key == "global":
        return data["Global"]
    else:
        for i in data["Countries"]:
            keyl = key.lower()
            if i["Country"].lower() == keyl or i["CountryCode"].lower() == keyl or i["Slug"].lower() == keyl:
                return i

        raise CountryNotFound(f"{key} bulunamadı")

def get_global():
    return requests.get(BASE_URL).json()["Global"]

def get_country(country):
    j = requests.get(BASE_URL).json()
    country = country.lower()

    for i in j["Countries"]:
        if i["Country"].lower() == country or i["CountryCode"].lower() == country or i["Slug"].lower() == country:
            return i

    raise CountryNotFound(f"{country} bulunamadı")


class Updater(threading.Thread):
    def __init__(self):
        super().__init__()
        self.alive = True
        self.summary = dict()
        self.interval = 28 * 60 #28 dakika

    def run(self):
        while self.alive:
            ok = False
            while not ok:
                try:
                    r = get_all()
                    self.summary = r
                    ok = True
                except Exception as e:
                    print("COVID19 API: " + e)
                    time.sleep(10)

            time.sleep(self.interval)


updater = Updater()
updater.start()
