# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import re
import selenium
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import json
import jieba
from wordcloud import WordCloud, ImageColorGenerator
from collections import Counter
import os
import cv2
from pyecharts import Bar,Geo,Line,Overlap,Radar
from pyecharts import configure
import matplotlib.image as mpimg
from urllib.request import  urlopen  
from urllib  import request  

os.chdir('D:/爬虫/惊为天人')

# 开始爬取数据
driver = webdriver.Chrome()
driver.maximize_window()
url = 'https://www.zhihu.com/question/291506148'
js='window.open("'+url+'")'
driver.execute_script(js)
for i in range(1000):
     time.sleep(1)
     js="var q=document.documentElement.scrollTop=10000000"  
     driver.execute_script(js)
     print(i)

# 整理ID
all_html = [k.get_property('innerHTML') for k in driver.find_elements_by_class_name('AnswerItem')]
all_text = ''.join(all_html)
pat = '/space.bilibili.com/\d+'
spaces = list(set([k for k in re.findall(pat,all_text)]))


# 获得信息
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win32; x32; rv:54.0) Gecko/20100101 Firefox/54.0',
'Connection': 'keep-alive'}
cookies ='v=3; iuuid=1A6E888B4A4B29B16FBA1299108DBE9CDCB327A9713C232B36E4DB4FF222CF03; webp=true; ci=1%2C%E5%8C%97%E4%BA%AC; __guid=26581345.3954606544145667000.1530879049181.8303; _lxsdk_cuid=1646f808301c8-0a4e19f5421593-5d4e211f-100200-1646f808302c8; _lxsdk=1A6E888B4A4B29B16FBA1299108DBE9CDCB327A9713C232B36E4DB4FF222CF03; monitor_count=1; _lxsdk_s=16472ee89ec-de2-f91-ed0%7C%7C5; __mta=189118996.1530879050545.1530936763555.1530937843742.18'
cookie = {}
for line in cookies.split(';'):
    name, value = cookies.strip().split('=', 1)
    cookie[name] = value


upstat = pd.DataFrame(columns=['name','fans','face','main_type','total_video',
                               'total_play', 'total_comment'])
for i in range(len(spaces)):
    try:
        time.sleep(1) 
        space_id = str(spaces[i].replace('/space.bilibili.com/',''))
        url= 'https://api.bilibili.com/x/web-interface/card?mid={}&jsonp=jsonp&article=true'.format(space_id)
        html = requests.get(url=url, cookies=cookie, headers=header).content
        data = json.loads(html.decode('utf-8'))['data']
        this_name = data['card']['name']
        this_fans = data['card']['fans']
        this_face = data['card']['face']
        this_video = int(data['archive_count'])
        total_page = int((this_video-1)/30)+1
        video_list=[]
        for j in range(total_page):               
            url = 'https://api.bilibili.com/x/space/arc/search?mid={}&ps=30&tid=0&pn={}&keyword=&order=click&jsonp=jsonp'.format(space_id,str(j+1))
            html = requests.get(url=url, cookies=cookie, headers=header).content
            data = json.loads(html.decode('utf-8'))
            if j == 0 :
                 type_list = data['data']['list']['tlist']
            this_list = data['data']['list']['vlist']
            video_list = video_list + [ this_list [k] for k in range(len(this_list))] 
        type_list = list(type_list.values())
        type_list = {type_list[k]['name']:int(type_list[k]['count']) for k in range(len(type_list))}
        this_type = max(type_list,key=type_list.get)
        this_play = sum([video_list[k]['play'] for k in range(len(video_list)) if video_list[k]['play'] != '--'])
        this_comment = sum([video_list[k]['comment'] for k in range(len(video_list)) if video_list[k]['comment'] != '--'])                             
        upstat = upstat.append({'name':this_name,
                               'fans':this_fans,
                               'face':this_face,
                               'main_type':this_type,
                               'total_video':this_video,
                               'total_play':this_play,
                               'total_comment':this_comment},
                              ignore_index=True)
        print('success:'+str(i))
    except:
        print('fail:'+str(j))
        continue

upstat['avg_comment'] = upstat['total_comment'] / upstat['total_video']
upstat['avg_play'] = upstat['total_play'] / upstat['total_video']
upstat['avg_danmu'] = upstat['total_danmu'] / upstat['total_video']





## 拼图
i = 0 
for filename in os.listdir("./CEOlogo"):
    head_loc = 'D:/爬虫/看准/公司logo/'+this_name+'.jpg'
    ceo_loc = 'D:/爬虫/看准/CEOlogo/'+this_name+'.jpg'

    file_loc = "D:/爬虫/看准/CEOlogo/"+filename
    img = mpimg.imread(file_loc)[:,:,0:3]
    img = cv2.resize(img, (500,500),interpolation=cv2.INTER_CUBIC)
    if i % 20 == 0:
        row_img=img
    elif i == 19:
        row_img=np.hstack((row_img,img))
        all_img = row_img
    elif i % 20 == 19:
        row_img=np.hstack((row_img,img))
        all_img = np.vstack((all_img,row_img))
    else:
        row_img=np.hstack((row_img,img))
    i = i+1
plt.imshow(all_img)    
plt.axis('off')








