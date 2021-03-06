#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: PanFei Liu
import os
def open_file(mode):
    """打开文件"""
    BASE_DIR = os.path.dirname(__file__)
    h_file = open(os.path.join(BASE_DIR, "data/haproxy.cfg"), mode, encoding="utf-8")
    return h_file

def bak_file():
    """修改前备份"""
    f = open_file("r")
    with open("data/haproxy.cfg.bak","w", encoding="utf-8") as f_bak:
        for line in f:
            f_bak.writelines(line)
    f.close()

def retrieve(string):
    """查询"""
    f = open_file('r')
    string = "backend " + string
    count = 0
    for line in f:
        if string in line and line[0] == 'b':
            count += 1
            print(line.rstrip())
        elif count == 1:
            count = 2
            print(line)
        else:
            pass
    if count == 0:
        print("What you find the configuration does not exist.")
    f.close()


def create(string):
    """新增"""
    dict_str = eval(string)
    # print(dict_str)
    bak_file()
    f = open_file('r+')

    string = "backend " + dict_str["backend"]
    count = 0 #是否已经存在配置的标记
    for line in f:
        if string in line and len(string) == len(line.rstrip()) and count == 0:
            #print(dict_file["bakend"] )
            print("Configuration has been... ")
            count = 1
            break

    if count == 0:
        str_bakend = "backend " + dict_str["backend"] + "\n"
        str_record = "\t\tserver " + dict_str["record"]["server"]\
                     + " weight " + str(dict_str["record"]["weight"])\
                     + " maxconn " + str(dict_str["record"]["maxconn"])

        # print(str_bakend, str_record)
        f.writelines("\n\n")
        f.writelines(str_bakend)
        f.writelines(str_record)
        f.close()
        print("Add success ...")

def delete(string):
    """删除"""
    dict_str = eval(string)
    # print(dict_str)
    bak_file()
    f_r = open_file('r')


    string = "backend " + dict_str["backend"]
    temp_str = []
    count = 0 #是否已经存在配置的标记
    for line in f_r:
        temp_str.append(line)
        if string in line and len(string) == len(line.rstrip()) and count == 0:
            count = 1
    f_r.close()

    f_w = open_file('w')
    if count == 1:
        # print(temp_str)
        sign = 0
        for i in temp_str:
            if string in i and len(string) == len(i.rstrip()):
                sign = 1
                continue
            elif sign == 1:
                sign = 0
                continue
            # print(i)
            f_w.writelines(i)
        print("Configuration deleted successfully.")

    else:
        for i in temp_str:
            f_w.writelines(i)
        print("what you want to delete the configuration does not exist.")
    f_w.close()

def haproxy_do():
    """增删查操作"""
    print("""
    -> 1 search
    -> 2 add
    -> 3 delete
    """)
    name = input("What do you want. >>> ")
    if name.isdigit():
        name = int(name)
        if name == 1:
            string = input("--> What do you retrieve. >>> ") #www.oldboy.org
            retrieve(string)
        elif name == 2:
            string = input("--> Input your arg. >>> ")
            create(string)
        elif name == 3:
            string = input("--> What do you delete the configuration. >>>")
            delete(string)
        else:
            print("Input is wrong...")
    else:
        print("Input is wrong...")



haproxy_do()

"""
{'backend': 'www.oldboy', 'record':{'server': '100.1.7.8', 'weight': 20, 'maxconn': 3000}}
"""
