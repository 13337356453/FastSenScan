import argparse
import os.path
import re
from datetime import datetime
from queue import Queue
import logging
import http
from Scanner import Scaaner

logging.captureWarnings(True)

http.client.HTTPConnection._http_vsn_str = 'HTTP/1.1'
URL_PATTERN=re.compile(r"https?:\/\/[a-zA-Z0-9-._~:/?#[\]@!$&'()*+,;=%]+")

def check():
    global target
    global target_type
    if threads<1 or threads>30:
        exit("不合理的线程数")
    if url!=None:
        if not re.match(URL_PATTERN,url):
            exit("不合理的URL输入")
        target=url
    else:
        if not os.path.exists(file):
            exit(file+"文件不存在")
        target=file
        target_type=1
    if not os.path.exists(dic):
        exit(dic+"文件不存在")
    if wait<1 or wait>30:
        exit("不合理的超时时间")
    return True


def main():
    if not os.path.exists("result"):
        os.mkdir("result")
    q=Queue()
    f=open(dic,"r",encoding='utf-8')
    paths=[x.strip() for x in f.readlines() if x.strip()!=""]
    f.close()
    if target_type==0:
        for path in paths:
            q.put(target+"/"+path)
    else:
        f=open(target,"r",encoding="utf-8")
        urls=[x.strip() for x in f.readlines() if x.strip()!=""]
        f.close()
        for url in urls:
            for path in paths:
                q.put(url+"/"+path)
    outname="result/"+datetime.now().strftime("%Y%m%d%H%M%S")+".txt"
    ts=[]
    for i in range(threads):
        ts.append(Scaaner(q,wait,cookie,outname))
    for t in ts:
        t.start()
    for t in ts:
        t.join()

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description="一款快速扫描敏感文件的工具")
    parser.add_argument("-u","--url",help="目标URL")
    parser.add_argument("-f","--file",help="目标列表文件")
    parser.add_argument("-t","--threads",help="线程数",type=int,default=10)
    parser.add_argument("-d","--dic",help="自定义目录文件",default="dic.txt")
    parser.add_argument("-w","--wait",help="自定义超时时间",type=int,default=10)
    parser.add_argument("-c","--cookie",help="自定义Cookie",default="")
    args=parser.parse_args()
    url=args.url
    file=args.file
    threads=args.threads
    dic=args.dic
    wait=args.wait
    cookie=args.cookie
    target=""
    target_type=0
    if check():
        main()
