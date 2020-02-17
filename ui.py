#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

'''
Name   : ui.py
Author : Modnar
Date   : 2020/02/08
Copyrights (c) 2020 Modnar. All rights reserved.
'''

import os, tkinter
import webbrowser
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import datasource

plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False

if not os.path.exists('cache/img/'):
    os.makedirs('cache/img/')

class MainWindow(object):
    '''
    窗口构造器:
    @param label: 窗口标题
    @param names: 名字列表(2维数组: 0维度为国家名称; 1维度为省级名称)
    '''
    def __init__(self, label, names):
        self.root = tkinter.Tk()
        self.root.title(label)
        self.names = names
        self.add_widgets()
        self.root.resizable(False, False)
        self.root.mainloop()


    '''
    窗口初始化函数:
        将窗口Frame以及Frame上的部件初始化并布局。
    '''
    def add_widgets(self):
        self.introduceFrame = ttk.Frame(self.root) # 程序标题显示面板
        self.countriesFrame = ttk.Frame(self.root) # 国家选项显示面板
        self.provincesFrame = ttk.Frame(self.root) # 省级选项显示面板
        self.operationFrame = ttk.Frame(self.root) # 程序操作显示面板
        self.introduceFrame.grid(padx=5, pady=5, row=0, column=0, sticky='nwe')
        self.countriesFrame.grid(padx=5, pady=5, row=1, column=0, sticky='nwe')
        self.provincesFrame.grid(padx=5, pady=5, row=2, column=0, sticky='nwe')
        self.operationFrame.grid(padx=5, pady=5, row=3, column=0, sticky='nwe')

        canvas_width = 730  # 画布宽度
        canvas_height = 280 # 画布高度
        self.canvas = tkinter.Canvas(self.introduceFrame, bg='lightblue', \
                width=canvas_width, height=canvas_height) 
        self.canvas.grid(padx=5, pady=5, row=0, column=0, sticky='nwes')
        im = Image.open('res/head.png')
        self.ph = ImageTk.PhotoImage(im)
        self.canvas.create_image(0, 0, image=self.ph, anchor=tkinter.NW)

        worldButton = ttk.Button(self.countriesFrame, text='国家级', \
                command=self.queryWorld)
        worldButton.grid(padx=3, pady=3, row=0, column=0)
        self.buttons = []   # 程序按钮集合(2维数组: 0维度为国家级；1维度为省级)
        buttonList = []
        for i in range(len(self.names[0])):
            buttonList.append(ttk.Button(self.countriesFrame, text=self.names[0][i], \
                    command=self.maker(i, 0)))
            buttonList[i].grid(padx=3, pady=3, row=i//8+1, column=i%8)
        self.buttons.append(buttonList.copy())

        chinaButton = ttk.Button(self.provincesFrame, text='省级', \
                command=self.queryChina)
        chinaButton.grid(padx=3, pady=3, row=0, column=0)
        buttonList.clear()
        for i in range(len(self.names[1])):
            buttonList.append(ttk.Button(self.provincesFrame, text=self.names[1][i], \
                    command=self.maker(i, 1)))
            buttonList[i].grid(padx=3, pady=3, row=i//8+1, column=i%8)
        self.buttons.append(buttonList.copy())

        ttk.Button(self.operationFrame, text='刷新', command=self.refresh) \
                .grid(padx=3, pady=3, row=0, column=0)
        ttk.Button(self.operationFrame, text='在浏览器打开原始网页', \
                command=self.open_in_browser) \
                .grid(padx=3, pady=3, row=0, column=1)


    '''
    选择程序闭包:
        用于记录每个按钮绑定的运行时执行函数。
    @param argv: 国家/省标号(从0到len(names[0/1])-1)
    @param choice: 标记选择的标号是国家级标号还是省级标号
    @return: 按钮具体绑定的运行时执行函数
    '''
    def maker(self, argv, choice):
        if choice == 0:
            def func1():
                self.queryCountry(argv)
            return func1
        else:
            def func2():
                self.queryProvince(argv)
            return func2


    '''
    国家级详情信息查询:
        用于执行国家级详情信息查询功能，即新建一个子窗口对数据进行可视化展示。
    @param argv: 国家标号(从0到len(names[0])-1)
    '''
    def queryCountry(self, argv):
        root = tkinter.Toplevel()
        name = self.names[0][argv]
        root.title('%s' % name)
        root.resizable(False, False)
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

        if argv == 0:
            canvas = tkinter.Canvas(chartFrame, bg='lightblue', width=470, height=350)
            canvas.grid(padx=5, pady=5, row=0, column=0, sticky='nwes')
            im = draw(data, name)
            ph = ImageTk.PhotoImage(im.resize((480, 360), Image.ANTIALIAS))
            canvas.create_image(0, 0, image=ph, anchor=tkinter.NW)
        else:
            pass

        root.mainloop()


    '''
    省级详情信息查询:
        用于执行省级详情信息查询功能，即新建一个子窗口对数据进行可视化展示。
    @param argv: 省标号(从0到len(names[1])-1)
    '''
    def queryProvince(self, argv):
        root = tkinter.Toplevel()
        name = self.names[1][argv]
        root.title('%s' % name)
        root.resizable(False, False)
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


    def queryWorld(self):
        root = tkinter.Toplevel()
        root.title('世界疫情数据')
        root.resizable(False, False)
        labelFrame = ttk.Frame(root)
        chartFrame = ttk.Frame(root)
        labelFrame.grid(padx=5, pady=5, row=0, column=0, sticky='nwe')
        chartFrame.grid(padx=5, pady=5, row=1, column=0, sticky='nwe')

        lastUpdateTime, data = datasource.world_data()
        ttk.Label(labelFrame, text="数据(中国)最近更新时间:\n%s" % \
                lastUpdateTime, width=52, foreground='green') \
                .grid(padx=5, pady=5, row=0, column=0, sticky='nwes')
        total_number = 0; china_number = data[0]['total']['confirm']
        for country in data:
            total_number += country['total']['confirm']
        text = "世界总确诊数: %d\n中国总确诊数: %d\n其余国家和地区总确诊数: %d" % \
                (total_number, china_number, total_number-china_number)
        ttk.Label(labelFrame, text=text, font='Helvetica -18', foreground='red') \
                .grid(padx=5, pady=5, row=1, column=0, sticky='nwes')

        canvas = tkinter.Canvas(chartFrame, bg='lightblue', width=900, height=350)
        canvas.grid(padx=5, pady=5, row=0, column=0, sticky='nwes')
        images = draw1(data)
        im0 = images[0]
        ph0 = ImageTk.PhotoImage(im0.resize((480, 360), Image.ANTIALIAS))
        canvas.create_image(0, 0, image=ph0, anchor=tkinter.NW)
        im1 = images[1]
        ph1 = ImageTk.PhotoImage(im1.resize((480, 360), Image.ANTIALIAS))
        canvas.create_image(440, 0, image=ph1, anchor=tkinter.NW)

        create_table(labelFrame, data).grid(padx=5, pady=10, row=0, column=1, \
                rowspan=2, sticky='e')

        root.mainloop()


    def queryChina(self):
        root = tkinter.Toplevel()
        root.title('中国疫情数据')
        root.resizable(False, False)
        labelFrame = ttk.Frame(root)
        chartFrame = ttk.Frame(root)
        labelFrame.grid(padx=5, pady=5, row=0, column=0, sticky='nwe')
        chartFrame.grid(padx=5, pady=5, row=1, column=0, sticky='nwe')

        data = datasource.china_data()
        ttk.Label(labelFrame, text="数据(中国)最近更新时间: %s" % \
                data['lastUpdateTime'], width=52, foreground='green') \
                .grid(padx=5, pady=5, row=0, column=0, sticky='nwes')
        d = data['total']
        ttk.Label(labelFrame, text='累计确诊: %d例'%d['confirm'], \
                font='Helvetica -18', foreground='purple') \
                .grid(padx=5, pady=2, row=1, column=0, sticky='nwes')
        ttk.Label(labelFrame, text='现有确诊: %d例'%d['nowConfirm'], \
                font='Helvetica -18', foreground='red') \
                .grid(padx=5, pady=2, row=2, column=0, sticky='nwes')
        ttk.Label(labelFrame, text='累计治愈: %d例'%d['heal'], \
                font='Helvetica -18', foreground='green') \
                .grid(padx=5, pady=2, row=3, column=0, sticky='nwes')
        ttk.Label(labelFrame, text='现有疑似: %d例'%d['suspect'], \
                font='Helvetica -18', foreground='orange') \
                .grid(padx=5, pady=2, row=4, column=0, sticky='nwes')
        ttk.Label(labelFrame, text='累计死亡: %d例'%d['dead'], \
                font='Helvetica -18', foreground='grey') \
                .grid(padx=5, pady=2, row=5, column=0, sticky='nwes')
        ttk.Label(labelFrame, text='现有重症: %d例'%d['nowSevere'], \
                font='Helvetica -18', foreground='magenta') \
                .grid(padx=5, pady=2, row=6, column=0, sticky='nwes')

        create_table(labelFrame, data['children']).grid(padx=5, pady=10, row=0, \
                column=1, rowspan=7, sticky='e')

        canvas = tkinter.Canvas(chartFrame, bg='lightblue', width=900, height=350)
        canvas.grid(padx=5, pady=5, row=0, column=0, sticky='nwes')
        images = draw2(data)
        im0 = images[0]
        ph0 = ImageTk.PhotoImage(im0.resize((480, 360), Image.ANTIALIAS))
        canvas.create_image(0, 0, image=ph0, anchor=tkinter.NW)
        im1 = images[1]
        ph1 = ImageTk.PhotoImage(im1.resize((480, 360), Image.ANTIALIAS))
        canvas.create_image(440, 0, image=ph1, anchor=tkinter.NW)

        root.mainloop()

    
    def refresh(self):
        datasource.refresh()
        messagebox.showinfo(title='REFRESH', message='数据刷新成功!')


    def open_in_browser(self):
        webbrowser.open('https://news.qq.com/zt2020/page/feiyan.htm?from=singlemessage')

'''
创造数据显示标签集合:
    用于展示国家级/省级数据，将四个标签作为一个列表返回。
'''
def create_labels(root, data):
    labels = []
    if 'suspect' in data['today']:
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
    else:
        labels.append(ttk.Label(root))
        labels[0]['text'] = '确诊\n%d' % data['total']['confirm']
        labels[0]['justify'] = 'center'
        labels[0]['foreground'] = 'red'
        labels.append(ttk.Label(root))
        labels[1]['text'] = '疑似\n%d' % data['total']['suspect']
        labels[1]['justify'] = 'center'
        labels[1]['foreground'] = 'orange'
        labels.append(ttk.Label(root))
        labels[2]['text'] = '死亡\n%d' % data['total']['dead']
        labels[2]['justify'] = 'center'
        labels[2]['foreground'] = 'grey'
        labels.append(ttk.Label(root))
        labels[3]['text'] = '治愈\n%d' % data['total']['heal']
        labels[3]['justify'] = 'center'
        labels[3]['foreground'] = 'green'
    return labels


def create_table(root, data, center=True):
    colums_name = ['地区', '确诊', '死亡', '治愈', '状态']
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

    img_name = 'cache/img/%s.png' % name
    plt.savefig(img_name)
    plt.close()
    image = Image.open(img_name)
    os.remove(img_name)
    return image


'''
绘制世界疫情数据图表:
    以饼状图来展示世界各个国家确诊数占比。
'''
def draw1(data):
    images = []

    labels = [data[0]['name'], '其余国家']
    others_total = 0
    for i in range(len(data)-1):
        others_total += data[1+i]['total']['confirm']
    nums = [data[0]['total']['confirm'], others_total]
    plt.pie(nums, labels=labels, autopct='%.2f%%', shadow=True)
    plt.title('世界疫情数据')
    img_name = 'cache/img/world_data.png'
    plt.savefig(img_name); plt.close()
    images.append(Image.open(img_name))
    # image = Image.open('cache/img/world_data.png')
    os.remove(img_name)

    labels = [item['name'] for item in data][1:11]
    nums = [item['total']['confirm'] for item in data][1:11]
    X = range(1, 11)
    plt.bar(X, nums, facecolor='red', edgecolor='white')
    for x, y in zip(X, nums):
        plt.text(x, y, '%d' % y, ha='center', va='bottom')
    nums = [item['total']['heal'] for item in data][1:11]
    plt.bar(X, nums, facecolor='green', edgecolor='white')
    for x, y in zip(X, nums):
        plt.text(x, y, '%d' % y, ha='center', va='center')
    plt.xticks(X, labels)
    patches = [mpatches.Patch(color='red', label='确诊'), \
            mpatches.Patch(color='green', label='治愈')]
    plt.legend(handles=patches, ncol=1, loc='best')
    plt.title('除中国外前10位国家地区疫情数据')
    img_name = 'cache/img/world_data_1.png'
    plt.savefig(img_name); plt.close()
    images.append(Image.open(img_name))
    os.remove(img_name)

    return images


def draw2(data):
    images = []

    X = [i for i in range(1, len(data['dayList'])+1)] 
    dates = []; confirms = []; suspects = []; deads = []; heals = []
    d = data['dayList']
    for day in d:
        dates.append(day['date'])
        confirms.append(day['confirm'])
        suspects.append(day['suspect'])
        deads.append(day['dead'])
        heals.append(day['heal'])
    plt.plot(X, confirms, color='red')
    plt.plot(X, suspects, color='orange')
    plt.plot(X, deads, color='grey')
    plt.plot(X, heals, color='green')
    for x, y in zip(X[::2], confirms[::2]):
        plt.text(x, y, '%d' % y, ha='center', va='center')
    plt.xticks(X[::2], dates[::2], rotation=45)
    patches = [mpatches.Patch(color='red', label='确诊'), \
            mpatches.Patch(color='orange', label='疑似'), \
            mpatches.Patch(color='grey', label='死亡'), \
            mpatches.Patch(color='green', label='治愈')]
    plt.legend(handles=patches, ncol=1, loc='best')
    plt.title('中国疫情数据走势')
    img_name = 'cache/img/china_data.png'
    plt.savefig(img_name); plt.close()
    images.append(Image.open(img_name))
    os.remove(img_name)

    X = [i for i in range(1, len(data['dayAddList'])+1)] 
    dates = []; confirms = []; suspects = []; deads = []; heals = []
    d = data['dayAddList']
    for day in d:
        dates.append(day['date'])
        confirms.append(day['confirm'])
        suspects.append(day['suspect'])
        deads.append(day['dead'])
        heals.append(day['heal'])
    plt.plot(X, confirms, color='red')
    plt.plot(X, suspects, color='orange')
    plt.plot(X, deads, color='grey')
    plt.plot(X, heals, color='green')
    for x, y in zip(X[::2], confirms[::2]):
        plt.text(x, y, '%d' % y, ha='center', va='center')
    plt.xticks(X[::2], dates[::2], rotation=45)
    patches = [mpatches.Patch(color='red', label='确诊增长数'), \
            mpatches.Patch(color='orange', label='疑似增长数'), \
            mpatches.Patch(color='grey', label='死亡增长数'), \
            mpatches.Patch(color='green', label='治愈增长数')]
    plt.legend(handles=patches, ncol=1, loc='best')
    plt.title('中国疫情增长走势')
    img_name = 'cache/img/china_data.png'
    plt.savefig(img_name); plt.close()
    images.append(Image.open(img_name))
    os.remove(img_name)

    return images
