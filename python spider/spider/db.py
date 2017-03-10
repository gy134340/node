import _thread
import time
import random
import math
import re
import requests
import pymysql
# import sql
from bs4 import BeautifulSoup
domain = 'https://book.douban.com'
baseUrl = 'https://book.douban.com/tag/'

types = {
	"小说": "novel",
	"随笔": "essay",
	"日本文学": "japan",
	"散文": "prose",
	"诗歌": "poetry",
	"童话": "fairytales",
	"名著": "masterpiece",
	"推理": "reasoning",
	"青春": "youth",
	"科幻": "science",
	"漫画": "cartoon",
	"武侠": "swordsman",
	"奇幻": "fantasy",
	"历史": "history",
	"哲学": "philosophy",
	"传记": "biography",
	"回忆录": "memoir",
	"励志": "selfimprovement",
	"旅行": "travel",
	"科普": "polularscience",
	"编程": "program",
	"互联网": "internet",
	"算法": "algorithm",
}

# mysql connect
global conn
def connect():
    global conn
    conn = pymysql.connect(host='127.0.0.1', port=8889, user='root', passwd='123456789', db='ibook', charset='utf8')

# mysql close
def close():
    global conn
    conn.close()

# 书籍详情页面
def getDeatailPage(url):
    # time.sleep(3)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

# 获取第一层页面，返回这一页和nextUrl
def getHtml(tag):
    global domain
    tagUrl = domain + tag
    r = requests.get(tagUrl)
    soup = BeautifulSoup(r.text, 'html.parser')
    # soup = getDeatailPage(tagUrl)
    books = soup.find_all('li', class_ = 'subject-item')
    # nextUrl = soup.select(".paginator .thispage")[0].find_next_sibling().get('href')

    if len(books) > 0:
        for book in books:
            name = book.h2.get_text()
            author = book.find('div', class_='pub').get_text().split('/')[0]
            rate = book.find('span', class_='rating_nums').get_text()
            # rate = int(rate)
            paticipant = book.find('span', class_='pl').get_text()
            paticipant = int(re.findall(r'\d+',paticipant)[0])
            img_url = book.find('div', class_='pic').img['src']
            url = book.find('div', class_='pic').a['href']
            intro_str = book.p.get_text()
            if book.p:
                intro = book.p.get_text()
            else:
                intro = ''

            detailSoup = getDeatailPage(url)
            author_arr = detailSoup.find_all('div', class_ = 'intro')
            if len(author_arr) > 1:
                author_intro = author_arr[1].get_text()
            else:
                author_intro = ''

            tags = detailSoup.select('#db-tags-section .indent span a')
            tag = []
            splitTag = '|'
            for sub in tags:
                tag.append(sub.get_text())
            tag = splitTag.join(tuple(tag))

            obj = {
                'name': name.strip(),
                'author':author.strip(),
                'rate':rate,
                'paticipant':paticipant,
                'img_url':img_url.strip(),
                'url':url.strip(),
                'intro':intro.strip(),
                'author_intro':author_intro.strip(),
                'tag':tag.strip(),
            }
            insert(obj)

        # getHtml(nextUrl) # get next page
        # print(nextUrl)
    else:
        return

# 插入
def insert(obj):
    global conn
    connect()
    cursor = conn.cursor()
    query = """INSERT INTO `novel` (`name`, `author`, `rate`, `paticipant`, `img_url`, `url`, `intro`, `author_intro`, `tag`)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    param = (obj['name'], obj['author'], obj['rate'], obj['paticipant'], obj['img_url'], obj['url'], obj['intro'], obj['author_intro'], obj['tag'])

    try:
        cursor.execute(query, param)
        conn.commit()
    except:
        conn.rollback()
        print('insert error')
    else:
        print('suceess', obj['name'])
    cursor.close()
    conn.close()

# @todo delete select update

# for type in types:
type = '/tag/小说'
getHtml(type)




# sql.connect()
# sql.close()


