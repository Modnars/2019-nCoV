#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

'''
Name   : ui.py
Author : Modnar
Date   : 2020/02/08
Copyrights (c) 2020 Modnar. All rights reserved.
'''

import os, tkinter
from tkinter import ttk
from PIL import Image, ImageTk

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import datasource

plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False

if not os.path.exists('cache/img/'):
    os.makedirs('cache/img/')

class MainWindow(object):

    def __init__(self, label, names):
        self.root = tkinter.Tk()
        self.root.title(label)
        self.names = names
        self.add_widgets()
        self.root.mainloop()


    def add_widgets(self):
        self.introduceFrame = ttk.Frame(self.root)
        self.countriesFrame = ttk.Frame(self.root)
        self.provincesFrame = ttk.Frame(self.root)
        self.operationFrame = ttk.Frame(self.root)
        self.introduceFrame.grid(padx=5, pady=5, row=0, column=0, sticky='nwe')
        self.countriesFrame.grid(padx=5, pady=5, row=1, column=0, sticky='nwe')
        self.provincesFrame.grid(padx=5, pady=5, row=2, column=0, sticky='nwe')
        self.operationFrame.grid(padx=5, pady=5, row=3, column=0, sticky='nwe')

        canvas_width = 730
        canvas_height = 280
        self.canvas = tkinter.Canvas(self.introduceFrame, bg='lightblue', \
                width=canvas_width, height=canvas_height) 
        self.canvas.grid(padx=5, pady=5, row=0, column=0, sticky='nwes')
        im = Image.open('res/head.png')
        self.ph = ImageTk.PhotoImage(im)
        self.canvas.create_image(0, 0, image=self.ph, anchor=tkinter.NW)

        self.buttons = []
        buttonList = []
        for i in range(len(self.names[0])):
            buttonList.append(ttk.Button(self.countriesFrame, text=self.names[0][i], \
                    command=self.maker(i, 0)))
            buttonList[i].grid(padx=3, pady=3, row=i//8, column=i%8)
        self.buttons.append(buttonList.copy())

        buttonList.clear()
        for i in range(len(self.names[1])):
            buttonList.append(ttk.Button(self.provincesFrame, text=self.names[1][i], \
                    command=self.maker(i, 1)))
            buttonList[i].grid(padx=3, pady=3, row=i//8, column=i%8)
        self.buttons.append(buttonList.copy())


    def maker(self, argv, choice):
        if choice == 0:
            def func1():
                self.queryCountry(argv)
            return func1
        else:
            def func2():
                self.queryProvince(argv)
            return func2


    def queryCountry(self, argv):
        root = tkinter.Toplevel()
        name = self.names[0][argv]
        root.title('%s' % name)
        labelFrame = ttk.Frame(root)
        chartFrame = ttk.Frame(root)
        labelFrame.grid(padx=5, pady=5, row=0, column=0, sticky='nwe')
        chartFrame.grid(padx=5, pady=5, row=1, column=0, sticky='nwe')

        data = datasource.countries(argv)
        isUpdatedLabel = ttk.Label(labelFrame)
        isUpdatedLabel['text'] = '今日已更新' if data['isUpdated'] else '今日未更新'
        isUpdatedLabel['foreground'] = 'green' if data['isUpdated'] else 'red'
        isUpdatedLabel.grid(padx=5, pady=5, row=0, column=0, columnspan=4, \
                sticky='nwes')

        labels = create_labels(labelFrame, data)
        for i in range(len(labels)):
            labels[i].grid(padx=18, pady=5, row=1, column=i, sticky='w')

        canvas = tkinter.Canvas(chartFrame, bg='lightblue', width=470, height=350) 
        canvas.grid(padx=5, pady=5, row=0, column=0, sticky='nwes')
        im = draw(data, name)
        ph = ImageTk.PhotoImage(im.resize((480, 360), Image.ANTIALIAS))
        canvas.create_image(0, 0, image=ph, anchor=tkinter.NW)

        root.mainloop()


    def queryProvince(self, argv):
        root = tkinter.Toplevel()
        name = self.names[1][argv]
        root.title('%s' % name)
        labelFrame = ttk.Frame(root)
        chartFrame = ttk.Frame(root)
        labelFrame.grid(padx=5, pady=5, row=0, column=0, sticky='nwe')
        chartFrame.grid(padx=5, pady=5, row=1, column=0, sticky='nwe')

        data = datasource.provinces(argv)
        isUpdatedLabel = ttk.Label(labelFrame)
        isUpdatedLabel['text'] = '今日已更新' if data['isUpdated'] else '今日未更新'
        isUpdatedLabel['foreground'] = 'green' if data['isUpdated'] else 'red'
        isUpdatedLabel.grid(padx=5, pady=5, row=0, column=0, columnspan=4, \
                sticky='nwes')

        labels = create_labels(labelFrame, data)
        for i in range(len(labels)):
            labels[i].grid(padx=18, pady=5, row=1, column=i, sticky='w')

        table = create_table(chartFrame, data['children'])
        table.grid(padx=5, pady=5, row=0, column=0, sticky='nwes')

        root.mainloop()


def create_labels(root, data):
    labels = []
    labels.append(ttk.Label(root))
    todayNum = data['today']['confirm']
    labels[0]['text'] = '确诊\n%d\n较昨日%s' % (data['total']['confirm'], \
            '+%d' % todayNum if todayNum >= 0 else '%d' % todayNum)
    labels[0]['justify'] = 'center'
    labels[0]['foreground'] = 'red'
    labels.append(ttk.Label(root))
    todayNum = data['today']['suspect']
    labels[1]['text'] = '疑似\n%d\n较昨日%s' % (data['total']['suspect'], \
            '+%d' % todayNum if todayNum >= 0 else '%d' % todayNum)
    labels[1]['justify'] = 'center'
    labels[1]['foreground'] = 'orange'
    labels.append(ttk.Label(root))
    todayNum = data['today']['dead']
    labels[2]['text'] = '死亡\n%d\n较昨日%s' % (data['total']['dead'], \
            '+%d' % todayNum if todayNum >= 0 else '%d' % todayNum)
    labels[2]['justify'] = 'center'
    labels[2]['foreground'] = 'grey'
    labels.append(ttk.Label(root))
    todayNum = data['today']['heal']
    labels[3]['text'] = '治愈\n%d\n较昨日%s' % (data['total']['heal'], \
            '+%d' % todayNum if todayNum >= 0 else '%d' % todayNum)
    labels[3]['justify'] = 'center'
    labels[3]['foreground'] = 'green'
    return labels


def create_table(root, data, center=True):
    colums_name = ['城市', '确诊', '死亡', '治愈', '状态']
    colums_width = [100, 80, 80, 80, 80]
    indices = ['col%d' % i for i in range(len(colums_name))]
    table = ttk.Treeview(root, show='headings', columns=tuple(indices))
    for i in range(len(colums_name)):
        label = 'col' + str(i)
        val = colums_width[i]
        if (center):
            table.column(label, width=val, anchor='center')
        else: 
            table.column(label, width=val, anchor='w')
        table.heading(label, text=colums_name[i])
    for i in range(len(data)):
        record = tuple([data[i]['name'], data[i]['total']['confirm'], \
                data[i]['total']['dead'], data[i]['total']['heal'], \
                '已更新' if data[i]['today']['isUpdated'] else '未更新'])
        table.insert('', i, values=record)
    return table # User should pack the table theirselves


def draw(data, name):
    colors = ['#d62728', '#ff7f0e', '#1f77b4', '#2ca02c']
    # X = ['确诊', '疑似', '死亡', '治愈']
    X = [2, 4, 6, 8]
    d = data['total']
    Y1 = [d['confirm'], d['suspect'], d['dead'], d['heal']]
    d = data['today']
    Y2 = [Y1[0]-d['confirm'], Y1[1]-d['suspect'], Y1[2]-d['dead'], Y1[3]-d['heal']]
    plt.xticks(X, ['确诊', '疑似', '死亡', '治愈'])
    X1 = [x-0.2 for x in X]
    plt.bar(X1, Y1, edgecolor='white', color=colors)
    #plt.bar(X, Y1, facecolor='#9999ff', edgecolor='white')
    X2 = [x+0.2 for x in X] 
    plt.bar(X2, Y2, edgecolor='white', color=colors)
    #plt.bar(X, Y2, facecolor='#ff9999', edgecolor='white')

    for x, y in zip(X1, Y1):
        plt.text(x, y, '目前: %d' % y, ha='center', va='bottom')
    for x, y in zip(X2, Y2):
        plt.text(x, y, '以往: %d' % y, ha='center', va='top')

    plt.savefig('cache/img/%s.png' % name)
    plt.close()
    return Image.open('cache/img/%s.png' % name)
