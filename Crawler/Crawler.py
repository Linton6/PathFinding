# coding : UTF-8
# 高速解释器该py程序时UTF-8编码的，源程序可以有中文
import requests
import csv
import random
import time
import socket
import http.client
# import urllib.request
from bs4 import BeautifulSoup

"""
requests：用来抓取网页的html源代码 
csv：将数据写入到csv文件中 
random：取随机数 
time：时间相关操作 
socket和http.client 在这里只用于异常处理 
BeautifulSoup：用来代替正则式取源码中相应标签中的内容 
urllib.request：另一种抓取网页的html源代码的方法，但是没requests方便（我一开始用的是这一种）
"""


def get_content(url, data=None):
    header = {  # header是requests.get的一个参数，目的是模拟浏览器访问
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235'
    }
    timeout = random.choice(range(80, 180))  # timeout是设定的一个超时时间，取随机数是因为防止被网站认定为网络爬虫。
    while True:
        try:
            rep = requests.get(url, headers=header, timeout=timeout)  # 然后通过requests.get方法获取网页的源代码
            rep.encoding = 'utf-8'  # rep.encoding = ‘utf-8’是将源代码的编码格式改为utf-8（不该源代码中中文部分会为乱码）
            break

        except socket.timeout as e:  # 一些异常处理
            print('3:', e)
            time.sleep(random.choice(range(8, 15)))

        except socket.error as e:
            print('4:', e)
            time.sleep(random.choice(range(20, 60)))

        except http.client.BadStatusLine as e:
            print('5:', e)
            time.sleep(random.choice(range(30, 80)))

        except http.client.IncompleteRead as e:
            print('6:', e)
            time.sleep(random.choice(range(5, 15)))

    return rep.text
    # return html_text


def get_data(html_text):
    final = []
    bs = BeautifulSoup(html_text, "html.parser")  # 创建BeautifulSoup对象
    body = bs.body  # 获取body部分
    data = body.find('div', {'id': '7d'})  # 找到id为7d的div
    ul = data.find('ul')  # 获取ul部分
    li = ul.find_all('li')  # 获取所有的li

    for day in li:  # 对每个li标签中的内容进行遍历
        temp = []
        date = day.find('h1').string  # 找到日期
        temp.append(date)  # 添加到temp中
        inf = day.find_all('p')  # 找到li中的所有p标签
        temp.append(inf[0].string, )  # 第一个p标签中的内容（天气状况）加到temp中
        if inf[1].find('span') is None:
            temperature_highest = None  # 天气预报可能没有当天的最高气温（到了傍晚，就是这样），需要加个判断语句,来输出最低气温
        else:
            temperature_highest = inf[1].find('span').string  # 找到最高温
            temperature_highest = temperature_highest.replace('℃', '')  # 到了晚上网站会变，最高温度后面也有个℃
        temperature_lowest = inf[1].find('i').string  # 找到最低温
        temperature_lowest = temperature_lowest.replace('℃', '')  # 最低温度后面有个℃，去掉这个符号
        temp.append(temperature_highest)  # 将最高温添加到temp中
        temp.append(temperature_lowest)  # 将最低温添加到temp中
        final.append(temp)  # 将temp加到final中

    return final


def write_data(data, name):
    file_name = name
    with open(file_name, 'a', errors='ignore', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(data)


if __name__ == '__main__':
    url = 'http://www.weather.com.cn/weather/101190401.shtml'
    html = get_content(url)
    result = get_data(html)
    write_data(result, 'weather.csv')
