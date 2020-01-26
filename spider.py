import init
import requests
import os 
from bs4 import BeautifulSoup 
import re
import datetime
import configparser

global header,init_link
header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
                'Cache-Control': 'max-age=0',
                'Connection': 'close',
                'Cookie': '',
                'Host': 'xxxxxxxxxs6qbnahsbvxbghsnqh4rj6whbyblqtnmetf7vell2fmxmad.onion',
                'Referer': 'http://xxxxxxxxxs6qbnahsbvxbghsnqh4rj6whbyblqtnmetf7vell2fmxmad.onion/entrance/login.php',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
init_link = 'http://xxxxxxxxxs6qbnahsbvxbghsnqh4rj6whbyblqtnmetf7vell2fmxmad.onion/'

def set_cookie():
    config = configparser.ConfigParser()                        #设置cookie值
    config.read('tor_init.ini',encoding='UTF-8')
    global PHPSESSID,userid
    PHPSESSID = config.get('tor','PHPSESSID')
    userid = config.get('tor','userid')
    header['Cookie'] = 'PHPSESSID={}; userid={}'.format(PHPSESSID,userid)
    #print(header)

def spider():
    print("~~~~~~~~开始爬取deepmix中文暗网信息！！！~~~~~~~~")
    res = requests.get(url="http://xxxxxxxxxs6qbnahsbvxbghsnqh4rj6whbyblqtnmetf7vell2fmxmad.onion/index.php", headers=header,proxies={"https": "{}://127.0.0.1:{}".format(init.proxy_rules,init.tor_sockets_port),"http":"{}://127.0.0.1:{}".format(init.proxy_rules,init.tor_sockets_port)})
    # test = open('***\\暗网爬虫.html','w',encoding='utf-8')
    # test.write(res.text)
    # test.close()

    soup = BeautifulSoup(res.content,'html.parser')
    sort = soup.findAll('a',attrs={'href':re.compile('^ea.php'),'class':'text_index_top'})                #抓取分类
    if ((len(list(sort)))!=0):
        print("----------共发现{}个栏目----------".format(len(list(sort))))
    else: 
        print("----------Cookie已过期，请在配置文件中替换Cookie后再次尝试----------")
    for i in sort:
        print("[+] title：{} ".format(i.text))
        position = make_new_folder(i.text)               #文件存放路径
        current_page,total_page = get_page(i.get('href'))
        #print("[+] 当前页数：{}，总页数：{}\n".format(current_page,total_page))
        for pages in range(1,total_page+1):
            article_title,article_link = get_article(pages,i.get('href'))
            #print(article_title,article_link)
            article_title = rewrite_title(article_title)
            for j in range(len(article_title)):
                article_path = open(position+'\\'+article_title[j]+'.html','wb')
                article_final_link = init_link + article_link[j]
                try:
                    res = requests.get(url = article_final_link,headers=header,proxies={"https": "{}://127.0.0.1:{}".format(init.proxy_rules,init.tor_sockets_port),"http":"{}://127.0.0.1:{}".format(init.proxy_rules,init.tor_sockets_port)})
                    article_path.write(res.content)
                    article_path.close()
                except Exception as e:
                    print("[-] 出现问题：")
                    pass
            print("[+] 第{}页已爬取.".format(pages))

def make_new_folder(title):
    date = str(datetime.date.today())
    final_path = init.default_path + '\\' + date + '\\' + title
    if not (os.path.exists(final_path)):
        #print(final_path)
        os.makedirs(final_path)                             #创建多级目录使用makedirs
    return (final_path)

def get_page(link):                           #获取每一个分块下的当前页数以及总页数
    final_link = init_link + link
    res = requests.get(url = final_link,headers = header,proxies={"https": "{}://127.0.0.1:{}".format(init.proxy_rules,init.tor_sockets_port),"http":"{}://127.0.0.1:{}".format(init.proxy_rules,init.tor_sockets_port)})
    soup = BeautifulSoup(res.content,'html.parser')
    current_page = soup.findAll('button',attrs={'style':'background-color: #f4511e;','class':'button_page'})             #当前页的颜色不同
    total_page = soup.findAll('span',attrs={'class':'button_page'})                     #最大的页数为总页数
    total_page_list=[]         #用于存放所有的页数，以取得其中的最大值作为总页数
    for i in current_page:
        current_page = int(i.text)
        break                                                               #因为存在两个相同的当前页数，故打印一个就退出
    for j in total_page:
        total_page_list.append(int(j.text))     
    total_page = max(total_page_list)
    return(current_page,total_page)

def get_article(current_page,link):                      #获取具体售卖链接的标题和网址
    final_link = init_link+link+'&pagea='+str(current_page)+'#pagea'         #构造url
    res = requests.get(url = final_link , headers = header ,proxies={"https": "{}://127.0.0.1:{}".format(init.proxy_rules,init.tor_sockets_port),"http":"{}://127.0.0.1:{}".format(init.proxy_rules,init.tor_sockets_port)})
    soup = BeautifulSoup(res.content,'html.parser')
    article_title_list = []                       #用于存放文章标题
    article_link_list = []                          #用于存放文章链接
    article = soup.findAll('a',attrs={'class':'text_p_link'})
    for i in article:
        if (i.text!='打开'):                        #网站中同一个地址有两个按钮，其中一个的标题为“打开”
            article_link_list.append(i.get('href'))
            article_title_list.append(i.text)
    #print(article_title_list,article_link_list)
    return (article_title_list,article_link_list)
    
def rewrite_title(article_title):               #去除标题中导致无法存储文件的敏感字符
    new_article_title = []                           
    for title in article_title:
        temp = title.replace('\\','').replace('/','').replace(':','').replace('*','').replace('?','').replace('"','').replace('<','').replace('>','').replace('|','')
        new_article_title.append(temp)
    return new_article_title
