import init                         #导入init.py文件
import spider

if __name__ == "__main__":
    init.read_ini()
    init.switch_ip()                #建立新的tor节点
    spider.set_cookie()             #设置cookie值
    spider.spider()