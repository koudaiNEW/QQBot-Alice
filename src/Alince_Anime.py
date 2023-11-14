import requests  
import Alince_Module
import time
from fake_useragent import UserAgent
from lxml import etree
from dateutil import rrule
from datetime import datetime


class Anime_Analysis():

    #更新番剧字典
    def Anime_Flash_Anime_Dict(self):
        global tree
        global Anime
        global title
        headers = {
            'User-Agent' : UserAgent().random,
            'cookie' : "busuanziId=2011B4497C2846B3B1ABE92402338779",
            'referer': 'https://yuc.wiki/202310/'
        }
        url = 'https://yuc.wiki/202310/'  #根据季度变化
        tree = etree.HTML(requests.get(url=url, headers=headers).text.replace('<br>', ''))  #去掉br换行符
        #爬取番剧列表
        title = tree.xpath("//article[@class='post-block']//div[@style='float:left']//td[@class='date_title_' or @class='date_title' or @class='date_title__']/text()")
        #更新番剧字典
        Anime = {} 
        for name in title:
            Anime[name] = {
                'name':name,  #番剧名称
                'time':tree.xpath("//article[@class='post-block']//div[@style='float:left']//td[text()=\""+ name +"\"]/../../../../div[@class='div_date']/p//text()"),  #更新时间
                'image':tree.xpath("//article[@class='post-block']//div[@style='float:left']//td[text()=\""+ name +"\"]/../../../../div[@class='div_date']/img/@src"),  #封面
                'copyright':tree.xpath("//article[@class='post-block']//div[@style='float:left']//td[text()=\""+ name +"\"]/../..//td[@style]//a/@href")  #版权方
                }
            #转换标准时间
            try:
                 Anime[name]['time'][0] = Anime[name]['time'][0][:-1]  #月日
                 Anime[name]['time'][1] = Anime[name]['time'][1][:-1]  #时分
                 year = 2023
                 mon = int(Anime[name]['time'][0].split('/')[0])
                 day = int(Anime[name]['time'][0].split('/')[1])
                 hour = int(Anime[name]['time'][1].split(':')[0])
                 minn = int(Anime[name]['time'][1].split(':')[1])
                 #搓个轮子
                 if hour > 23 :
                     hour -= 24
                     day += 1
                     if mon == 2:
                         if day > 29:
                             day = 1
                             mon += 1
                     elif mon in (1,3,5,7,8,10,12):
                         if day > 31:
                             day = 1
                             mon += 1
                     elif mon in (4,6,9,11):
                         if day > 30:
                             day = 1
                             mon += 1
                     if mon > 12:
                         year += 1
                 Anime[name]['time'] = datetime.strptime(str(year) +'-'+ str(mon) +'-'+ str(day) +' '+ str(hour) +':'+ str(minn) +':00', '%Y-%m-%d %H:%M:%S')
            except:
                pass
        #刷新推送标志
        Anime_Analysis.Anime_Flash_Push(self)

    #刷新推送标志
    def Anime_Flash_Push(self):
        for name in title:
            Anime[name]['ready_To_Push'] = 0
            Anime[name]['push_Flag'] = 0


    #轮询
    def Anime_Main(self):
        for name in title:
            try:
                if Anime[name]['time'] == []:
                    pass
                if (datetime.now() - Anime[name]['time']).days % 7 == 0 and Anime[name]['ready_To_Push'] == 0:
                    Anime[name]['ready_To_Push'] = 1
                elif (datetime.now() - Anime[name]['time']).days % 7 == 1:
                    Anime[name]['ready_To_Push'] = 0
                    Anime[name]['push_Flag'] = 0
            except:
                pass

    #读取模块全局变量
    def Anime_Data(self, get_Data):
        try:
            if get_Data == 'Anime':
                return Anime
            elif get_Data == 'title':
                return title
            elif get_Data == 'tree':
                return tree
            else :
                return None
        except:
            print('Anime模块全局变量读取错误', flush=True)





stop = 1
