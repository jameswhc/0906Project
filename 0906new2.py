# coding: utf-8

import sys
import os
import requests
from bs4 import BeautifulSoup
#import json
import configparser as Conf

class MYSITE :
    def __init__(self,siteurl,encoding = 'utf-8',headers = {}):
        if headers == {} :
            headers = { 'Accept':'text/html,application/xhtml;q=0.9,image/webp,*/*;q=0.8' ,
                        'Accept-Encoding':'gzip, deflate',
                        'Accept-Language':'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                        'Connection':'keep-alive',
#                        'Cookie':'ASPSESSIONIDSCQSTABC=LIFMIBDAKCPBIMNMLEMMPHHB' ,
#                        'Host':'www.ucppweb.com',
#                        'Upgrade-Insecure-Requests':'1',
                        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; ) Gecko/20100101 Firefox/65.0' 
                        }
        if siteurl != '':
            self.url = siteurl
            self.ressite = requests.get(self.url,headers = headers,timeout = 5)
            self.ressite.encoding = encoding
            self.get_soup()
    def get_soup(self):
        self.soup = BeautifulSoup(self.ressite.text,'html.parser')
        return self.soup
    def set_encoding (self,encoding) :
        self.ressite.encoding = encoding
        self.get_soup()
    def set_url (self,siteurl) :
        if siteurl != '':
            self.url = siteurl
            self.ressite = requests.get(self.url,timeout = 5)
            self.get_soup()

def LINE_notify (token, msg):
#    發送 Line Notify 訊息
#    token 是發行權杖
#    msg 是要發送的訊息
    url = "https://notify-api.line.me/api/notify"
    headers = { \
            "Authorization": "Bearer " + token \
            ,"Content-Type" : "application/x-www-form-urlencoded" \
            }
        
    payload = {'message': msg}
    r = requests.post(url, headers = headers, params = payload)
    return r.status_code

def chk_SerchWeb (Name,url,LookingWord) :
    global Targets
    global ExSites
    Res_flag = 0
    found  = ''
    try :
        res = MYSITE (url)
        i = 0
        while True:
            a = res.soup.select (LookingWord[0])[LookingWord[1]+i]
#        print (str(a))
            found = BeautifulSoup (str (a),'html.parser').select ('a')[0]['href']
            i += 1
            stop = True
            at = a.text.lower()
            for tar in Targets :
                if at.find(tar) != -1:
                    for esite in ExSites:
                        if esite in found :
                            Res_flag = 0
                            stop = False
                            break
                        else :
                            Res_flag = 1
                    break
            if stop :
                break
    except Exception as e:
        Res_flag = 2
    finally :
        if Res_flag == 0 :
            Results = ""
        elif Res_flag == 2:
            Results = u"{} 服務異常，無法檢測\t".format(Name)
        else :
            Results = u"{} 找到疑似文件 - {}\t".format(Name,found)
        return Results


def __main__ ():
    global Targets
    global ExSites
    AppPath = ''
    configfile = ''
    if len (sys.argv) > 1  :
        arg = sys.argv[1]
        if (os.path.isdir(arg)) :
            AppPath = arg
        elif (os.path.isfile(arg)):
            AppPath = os.path.dirname(arg)
            configfile = arg
    if AppPath == '':
        AppPath = os.getcwd()
    if configfile == '' :
        configfile = '{}\\0906new.ini'.format(AppPath)
    if not (os.path.exists (configfile)) :
        print ('{}設定檔找不到'.format(configfile))
        return 1
    Config = Conf.ConfigParser(allow_no_value=True)
    Config.optionxform = str
    Config.read(configfile)
    tars = Config.items('Targets')
    Targets = []
    for tar in tars :
        Targets.append(tar[1])
#    f = open( configfile , 'r')
#    chk_word = json.load(f)
    ExSites = []
    for exclude in Config.items('EXCLUDE SITE') :
        ExSites.append(exclude[1])
    t_sites = Config.items('Sites')
    URLs = {}
    chk_word = {}
    for t_site in t_sites :
        searchs = Config.items('Searching')
        search = []
        for t_search in searchs :
            search.append(Config.get(t_site[1],'url')+t_search[1])
        t_url = {t_site[1] : search }
        URLs.update(t_url)
        t_look = {t_site[1] : [Config.get(t_site[1],'Looking word'),Config.getint(t_site[1],'Looking Raw')]}
        chk_word.update(t_look)
    Results = ''
    for web in URLs:
        for i in range(len(URLs[web])) :
            temp = chk_SerchWeb (web,URLs[web][i],chk_word[web])
            if (temp != '') :
                Results = Results + temp
                break
    if Results == "" :
        Results = u"今日三大搜尋網未有新連結"
#    print (Config['LINE']['Token'])
    LINE_notify (Config['Line']['Token'],Results)
#    print (Results)

    return 0 

Targets = []
ExSites = []

if __name__ == '__main__' :
    if __main__() == 0 :
        print ('Finished...')
    else :
        print ('程式異常終止.....')
