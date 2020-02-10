#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

'''
Name:   crawler.py
Author: Modnar
Date:   2020/02/08
Copyrights (c) 2020 Modnar. All rights reserved.
'''

import json, os, requests, time

if not os.path.exists('cache/'):
    os.makedirs('cache/')

def save():
    # Construct the request URL.
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=jQuery34107611450150347083_1580736608778&_=%d'%int(time.time()*1000)
    # Transform the request result (bytes) to string.
    content = str(requests.get(url=url).content, encoding='utf8')
    # Intercept the json format data.
    content = content[content.index('{'):-1]
    # Save the raw request contents as cache.
    with open('cache/data.json', 'w', encoding='utf-8') as writeFile:
        writeFile.write(content)
    # Get the data segment.
    data = json.loads(content)['data']
    data = json.loads(data)
    countries = data['areaTree']
    print(len(countries))
    for country in countries:
        print(country['name'])
    country = countries[0]
    print(country['name'])
    provinces = country['children']
    for province in provinces:
        print(' ', province['name'])
        cities = province['children']
        for city in cities:
            print('   %s  %d %d %d %d' % (city['name'], city['total']['confirm'], \
                    city['total']['suspect'], city['total']['dead'], \
                    city['total']['heal']))


'''
获取“武汉新型冠状病毒疫情”最新病情数据，并将数据以字典格式返回
数据获取来源:
    腾讯新闻报道数据
字典格式(更新于2020/02/09):
    {
        "lastUpdateTime": String,       // 格式: "2020-02-09 13:44:50"
        "chinaTotal": {
            "confirm": Int,
            "suspect": Int,
            "dead": Int,
            "heal": Int
        },
        "chinaAdd": {
            "confirm": Int,
            "suspect": Int,
            "dead": Int,
            "heal": Int
        },
        "isShowAdd": Bool
        "chinaDayList": [
        {
            "confirm": Int,
            "suspect": Int,
            "dead": Int,
            "heal": Int,
            "deadRate": String,         // "2.4"
            "healRate": String,         // "0.0"
            "date": String              // "01.13"
        },
        ...
        ]
        "chinaDayAddList": [
        {
            "confirm": Int,
            "suspect": Int,
            "dead": Int,
            "heal": Int,
            "deadRate": String,         // "0.0"
            "healRate": String,         // "0.0"
            "date": String              // "01.20"
        },
        ...
        ]
        "areaTree": [                   // 国家地区列表
        {
            "name": String,             // "中国"
            "today": {
                "confirm": Int,
                "suspect": Int,
                "dead": Int,
                "heal": Int
                "isUpdated": Bool
            },
            "total": {
                "confirm": Int,
                "suspect": Int,
                "dead": Int,
                "heal": Int
            },
            "children": [               // 省列表
            {
                "name": String,         // "湖北"
                "today": {
                    "confirm": Int,
                    "suspect": Int,
                    "dead": Int,
                    "heal": Int
                    "isUpdated": Bool
                },
                "total": {
                    "confirm": Int,
                    "suspect": Int,
                    "dead": Int,
                    "heal": Int
                },
                "children": [               // 城市列表
                {
                    "name": String          // "武汉"
                    "today": {
                        "confirm": Int,
                        "suspect": Int,
                        "dead": Int,
                        "heal": Int
                        "isUpdated": Bool
                    },
                    "total": {
                        "confirm": Int,
                        "suspect": Int,
                        "dead": Int,
                        "heal": Int
                    },
                },
                ...
                ]
            },
            ...
            ]
        },
        {
            "name": String,     // "日本": 除中国外，其他国家或地区均只显示国家级数据
            "today": {
                "confirm": Int,
                "suspect": Int,
                "dead": Int,
                "heal": Int
                "isUpdated": Bool
            },
            "total": {
                "confirm": Int,
                "suspect": Int,
                "dead": Int,
                "heal": Int
            },
        },
        ...
        ]
        "articleList": [
        {
            "cmsId": String,        // "20200209A0AG2G00"
            "source": String,       // "push"
            "media": String,        // "上海发布"
            "publish_time": String, // "2020-02-09 13:33:22"
            "can_use": Int,         // 1
            "desc": String,         // "2月9日0-12时，上海新增新型冠状病毒感染..."
            "url": String,          // "https://view.inews.qq.com/a/20200209A0AG2G00"
            "title": String         // "上海新增1例新冠肺炎确诊病例"
        }
        ...
        ]
    }
'''
def request():
    # Construct the request URL.
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=jQuery34107611450150347083_1580736608778&_=%d' % int(time.time()*1000)
    # Transform the request result (bytes) to string.
    content = str(requests.get(url=url).content, encoding='utf8')
    # Intercept the json format data.
    content = content[content.index('{'):-1]
    # Save the raw request contents as cache.
    # with open('cache/RequestContents.log', 'w', encoding='utf-8') as writeFile:
    #     writeFile.write(content)
    # Get the data segment (string).
    data = json.loads(content)['data']
    # Save the `data` segment from request result.
    # (used by `data.json` which could be parsed by online json parsing tools)
    with open('cache/data.cache', 'w', encoding='utf-8') as writeFile:
        writeFile.write(data)
    # Return the data (dict).
    return json.loads(data)

def main():
    data = request()
    print(type(data['chinaTotal']))
    print(type(data['areaTree']))
    print(type(data['areaTree'][0]))
    print(type(data['areaTree'][0]['today']))
    print(type(data['areaTree'][0]['children']))
    print(type(data['areaTree'][0]['children'][0]))
    print(type(data['areaTree'][0]['children'][0]['children']))
    print(type(data['areaTree'][0]['children'][0]['children'][0]))

if __name__ == '__main__': main()
