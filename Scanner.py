from threading import Thread

import requests
HEADERS={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",

}
def scan(url,wait,cookie,outfile):
    HEADERS["Cookies"]=cookie
    try:
        r=requests.get(url,headers=HEADERS,timeout=wait,verify=False)
        if r.status_code!=404:
            print(url)
            with open(outfile,"a+",encoding="utf-8") as f:
                f.write(url+"\n")
            return True
    except Exception as e:
        print(e)
    return False

class Scaaner(Thread):
    def __init__(self,q,wait,cookie,outfile):
        super().__init__()
        self.q=q
        self.wait=wait
        self.cookie=cookie
        self.outfile=outfile
    def run(self):
        while not self.q.empty():
            url=self.q.get()
            scan(url,self.wait,self.cookie,self.outfile)

