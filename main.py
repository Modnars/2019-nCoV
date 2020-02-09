#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

import datasource
import ui

def main():
    ui.MainWindow('2019-nCoV', datasource.names())

if __name__ == '__main__':
    main()
