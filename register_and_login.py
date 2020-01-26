import requests
import init
from bs4 import BeautifulSoup
import urllib
from aip import AipOcr
import ocr

global header,init_link
header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'xxxxxxxxxs6qbnahsbvxbghsnqh4rj6whbyblqtnmetf7vell2fmxmad.onion',
            'Referer': 'http://xxxxxxxxxs6qbnahsbvxbghsnqh4rj6whbyblqtnmetf7vell2fmxmad.onion/entrance/login.php',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}

init_link = 'http://deepmix2z2ayzi46.onion/'

def route():                                #在注册前需要访问route.php，以防直接访问注册页面地址失效
    print("——————————访问主界面——————————")
    res = requests.get(url=init_link,headers=header,proxies={"https": "{}://127.0.0.1:{}".format(init.proxy_rules,init.tor_sockets_port),"http":"{}://127.0.0.1:{}".format(init.proxy_rules,init.tor_sockets_port)})
    temp = 0
    while res.status_code!=200:
        print("[-] 加载注册页面失败，正在重新加载***")
        temp +=1
        if temp == 5:
            print("[-] 网络也许有问题，请重新进行配置")
            break
        res = requests.get(url=final_link,headers=header,proxies={"https": "{}://127.0.0.1:{}".format(init.proxy_rules,init.tor_sockets_port),"http":"{}://127.0.0.1:{}".format(init.proxy_rules,init.tor_sockets_port)})
    soup = BeautifulSoup(res.content,'html.parser')
    img = soup.findAll('img',attrs={'title':'只能刷新页面换验证码, 为安全因素去除了js代码, 无法点此刷新'})
    for i in img:
        pass
        #print(i.get('src'))
    picture_link = i.get('src')                     #验证码地址
    picture_local_link = save_picture(picture_link)
    text1 = ocr.main(picture_local_link)=='' ? '':ocr.main(picture_local_link)
    text2 = Identify(picture_local_link)==''  '':Identify(picture_local_link)
    route_header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
                    'Cache-Control': 'max-age=0',
                    'Connection': 'keep-alive',
                    'Content-Length': '65',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Cookie': 'PHPSESSID=v6uplodl8gp57qst14idjjvo6f; random=1042',
                    'Host': 'deepmix2z2ayzi46.onion',
                    'Origin': 'http://deepmix2z2ayzi46.onion',
                    'Referer': 'http://deepmix2z2ayzi46.onion/index.php',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    print(text1,text2)

def save_picture(picture_link):                                 #保存验证码图片
    res = requests.get(url=picture_link,headers=header,proxies={"https": "{}://127.0.0.1:{}".format(init.proxy_rules,init.tor_sockets_port),"http":"{}://127.0.0.1:{}".format(init.proxy_rules,init.tor_sockets_port)})
    file = open('***\\Verification.jpg','wb')
    file.write(res.content)
    file.close()
    print("[+] 验证码已保存到\"***\\Verification.jpg\"")
    return ('***\\Verification.jpg')

def Identify(picture_local_link):                                 #通过百度API识别验证码
    APP_ID = '18343289'
    API_KEY =  'l05IzKWSCd1FXgCtPdjo9vAG'
    SECRET_KEY = 'qomwMYzlCBGIecOiQ7rtGBff5GXwMX9N'
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    file = open (picture_local_link,'rb')
    image = file.read()
    ''' 可选参数 '''
    options = {}
    options["language_type"] = "ENG"  # 中英文混合
    options["detect_direction"] = "true"  # 检测朝向
    options["detect_language"] = "false"  # 是否检测语言
    options["probability"] = "false" 
    
    result = client.basicGeneral(image, options)
    file.close()
    if 'words_result' in result:
        text = ('\n'.join([w['words'] for w in result['words_result']]))
    exclude_char_list = ' .:\\|\'\"?![],()~@#$%^&*_+-={};<>/¥'
    text = ''.join([x for x in text if x not in exclude_char_list])
    #print(type(result), "和", type(text))
    print("百度API识别结果为：",text)
    return (text)


if __name__ == "__main__":
    init.read_ini()
    route()
