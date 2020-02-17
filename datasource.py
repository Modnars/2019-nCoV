#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

'''
Name   : datasource.py
Author : Modnar
Date   : 2020/02/09
Copyrights (c) 2020 Modnar. All rights reserved.
'''

import crawler

data = None

def refresh():
    global data
    data = crawler.request()


def names():
    names = []
    countryNames = []
    provinceNames = []
    for country in data['areaTree']:
        countryNames.append(country['name'])
    names.append(countryNames)
    for province in data['areaTree'][0]['children']:
        provinceNames.append(province['name'])
    names.append(provinceNames)
    return names
    

def world_data():
    dics = []
    for country in data['areaTree']:
        dic = {}
        dic['name'] = country['name']
        dic['today'] = country['today']
        dic['total'] = country['total']
        dics.append(dic)
    return (data['lastUpdateTime'], dics)


def china_data():
    dic = dict()
    dic['lastUpdateTime'] = data['lastUpdateTime']
    dic['total'] = data['chinaTotal']
    dic['dayList'] = data['chinaDayList']
    dic['dayAddList'] = data['chinaDayAddList']
    dic['children'] = data['areaTree'][0]['children']
    return dic


def countries(idx):
    dic = dict()
    dic['name'] = data['areaTree'][idx]['name']
    if idx == 0:
        dic['isUpdated'] = True
        dic['today'] = data['chinaAdd']
        dic['today']['suspect'] = data['chinaDayAddList'][-1]['suspect']
        #dic['today'] = data['chinaDayAddList'][-1]
        dic['total'] = data['chinaTotal']
    else:
        dic['isUpdated'] = data['areaTree'][idx]['today']['isUpdated']
        dic['today'] = data['areaTree'][idx]['today']
        dic['total'] = data['areaTree'][idx]['total']
    return dic


def provinces(idx):
    dic = dict()
    dic['name'] = data['areaTree'][0]['children'][idx]['name']
    dic['isUpdated'] = data['areaTree'][0]['children'][idx]['today']['isUpdated']
    dic['today'] = data['areaTree'][0]['children'][idx]['today']
    dic['total'] = data['areaTree'][0]['children'][idx]['total']
    dic['children'] = data['areaTree'][0]['children'][idx]['children']
    return dic


# Initialize the program with `refresh`.
refresh()
