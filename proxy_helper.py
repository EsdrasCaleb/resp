from fp.fp import FreeProxy
import requests
import random

class proxy_helper(object):
    def __init__(self,extra_source):
        self.sources = [{"url": "https://proxylist.geonode.com/api/proxy-list?protocols=socks4&limit=500&page=1&sort_by=lastChecked&sort_type=desc", "json":True,"protocol":""},
                        {
                            "url": "https://proxylist.geonode.com/api/proxy-list?protocols=Csocks5&limit=500&page=1&sort_by=lastChecked&sort_type=desc",
                            "json": True, "protocol": ""},
    {"url": "https://proxylist.geonode.com/api/proxy-list?protocols=http%2Chttps&limit=500&page=1&sort_by=lastChecked&sort_type=desc", "json": True, "protocol": ""},
    {"url": "https://www.proxy-list.download/api/v1/get?type=https","json":False,"protocol":"https"},
    {"url": "https://www.proxy-list.download/api/v1/get?type=http", "json": False,
                         "protocol": "http"},
    {"url": "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt","json":False,"protocol":"socks4"},
    {"url": "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt","json":False,"protocol":"socks5"}]
        if(extra_source):
            self.sources += extra_source
        self.black_list = []
        self.list = []
        self.currentIndex = 0

    def get_requested(self,source, json=False, protocol="http"):
        data = requests.get(source)
        retorno = []
        if (json):
            for i in data.json()["data"]:
                protIndex = 0
                while protIndex < len(i["protocols"]):
                    if (i["protocols"][protIndex] == "http"):
                        protIndex += 1
                    else:
                        break
                proxy = i["protocols"][protIndex] + "://" + i["ip"] + ":" + i["port"]
                if (proxy not in self.black_list):
                    retorno.append(proxy)
        else:
            for i in data.text.replace('\r\n', '\n').split('\n'):
                if (i):
                    proxy = protocol + "://" + i
                    if (proxy not in self.black_list):
                        retorno.append(proxy)
        return retorno

    def load_list(self):
        returnlist =[]
        while len(returnlist) ==0:
            dice = random.randint(0, len(self.sources) - 1)
            try:
                returnlist = self.get_requested(self.sources[dice]["url"], self.sources[dice]["json"], self.sources[dice]["protocol"])
            except Exception as e:
                returnlist = []
                print(e)
            if(len(returnlist) == 0):
                del self.sources[dice]
        self.list += returnlist
    def get_proxy(self):
        proxy = None
        try:
            proxy = FreeProxy(https=True).get()
            if(proxy in self.black_list):
                proxy = None
        except Exception as e:
            print(e)
            proxy = None
        try:
            proxy = FreeProxy(google=True).get()
            if(proxy in self.black_list):
                proxy = None
        except Exception as e:
            print(e)
            proxy = None
        if(not proxy):
            if(len(self.list) == 0):
                self.load_list()
                self.currentIndex = 0
            if(self.currentIndex >= len(self.list)):
                self.currentIndex = 0
            print("Proxy index :"+str(self.currentIndex))
            proxy = self.list[self.currentIndex]
            self.currentIndex += 1
        print("got proxy: " + proxy)
        return proxy

    def black_list_proxy(self,proxy):
        if (proxy not in self.list):
            self.black_list.append(proxy)
        if(proxy in self.list):
            self.list.remove(proxy)
