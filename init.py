from stem import Signal                 #tor的控制工具
from stem.control import Controller
import requests
from bs4 import BeautifulSoup           #爬虫库
import os
import datetime
import configparser                #读取ini文件
import re

def read_ini():
    config = configparser.ConfigParser()
    config.read('tor_init.ini',encoding='UTF-8')
    global tor_listener_port,tor_sockets_port,proxy_rules,default_path,header

    tor_listener_port = config.get('tor','tor_listener_port')
    tor_sockets_port = config.get('tor','tor_sockets_port')
    proxy_rules = config.get('tor','proxy_rules')
    default_path = config.get('file','default_path')

    header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
        }

def switch_ip():                      #切换TOR节点
    try:
        controller = Controller.from_port(port=int(tor_listener_port))            #9151为tor的监听端口
        controller.authenticate()
        controller.signal(Signal.NEWNYM)
        resp = requests.get(url="https://check.torproject.org/?lang=zh_CN", headers=header,proxies={"https": "{}://127.0.0.1:{}".format(proxy_rules,tor_sockets_port),"http":"{}://127.0.0.1:{}".format(proxy_rules,tor_sockets_port)})
        soup = BeautifulSoup(resp.content,'lxml')
        print('[+] '+soup.find('h1').text.replace("\n", "").replace(' ',''))               #删除输出中的换行符和空格
        print('[+] '+soup.find('p').text)
        make_new_path()                                         #如果代理成功则创建爬虫目录
    except Exception as e:
        print("[-] Error，请重新配置tor_init.ini")
        raise
    finally:
        controller.close()

def make_new_path():                     #生成新的文件存放目录。以日期为文件夹名
    if not (os.path.exists(default_path)):
        os.mkdir(default_path)



