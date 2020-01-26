import configparser

header = {'cookie':''}
config = configparser.ConfigParser()
config.read('tor_init.ini',encoding='UTF-8')
global PHPSESSID,userid
PHPSESSID = config.get('tor','PHPSESSID')
userid = config.get('tor','userid')
header['cookie'] = 'PHPSESSID={}; userid={}'.format(PHPSESSID,userid)
print(header)