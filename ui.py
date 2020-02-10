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
        canvas_height = 320
        self.canvas = tkinter.Canvas(self.introduceFrame, bg='lightblue', \
                width=canvas_width, height=canvas_height) 
        self.canvas.grid(padx=5, pady=5, row=0, column=0, sticky='nwes')
        im = Image.open('res/head.png')
        self.ph = ImageTk.PhotoImage(im)
        self.canvas.create_image(canvas_width/2, canvas_height/2, 
                image=self.ph, anchor='center')

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
        name = self.buttons[0][argv]['text']
        root.title('%s' % name)
        labelFrame = ttk.Frame(root)
        chartFrame = ttk.Frame(root)
        labelFrame.grid(padx=5, pady=5, row=0, column=0, sticky='nwe')
        chartFrame.grid(padx=5, pady=5, row=1, column=0, sticky='nwe')

        canvas = tkinter.Canvas(chartFrame, bg='lightblue', width=640, height=480) 
        canvas.grid(padx=5, pady=5, row=0, column=0, sticky='nwes')
        data = datasource.countries(argv)
        im = draw(data, name)
        ph = ImageTk.PhotoImage(im.resize((480, 360), Image.ANTIALIAS))
        canvas.create_image(320, 240, image=ph, anchor='center')
        root.mainloop()


    def queryProvince(self, argv):
        root = tkinter.Toplevel()
        root.title('%s' % self.buttons[1][argv]['text'])


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
