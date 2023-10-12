import csv
import random

import numpy as  np
# 时间窗：【0,840】
# 地理坐标：【0-180,0-180】
# [0,360],[-180,180]
# 编号 坐标 时间窗 重量

def gen(I):
    n = random.randint(10,100)
    data = []
    # deport_x = np.random.randint(0, 360)
    # deport_y = np.random.randint(-180, 180)
    dep = []
    # dep.append(deport_x)
    # dep.append(deport_y)
    dep.append(n)
    data.append(dep)
    # 0 : 仓库，[1,n] : 用户
    for i in range(0, n + 2):
        t = []
        # 编号
        number = i
        # 坐标
        x = np.random.randint(0, 360)
        y = np.random.randint(-180, 180)
        # 时间窗
        tl = np.random.randint(0, 840)
        tr = np.random.randint(tl, 840)
        # 载货量
        q = np.random.randint(0, 100)
        # 服务时间
        s = np.random.randint(10,30)
        # 如果是仓库
        if(i == 0):
            tl = 0
            tr = 840
            q = 0
            s = 0
        if(i == n + 1):
            x = data[1][1]
            y = data[1][2]
            tl = 0
            tr = 840
            q = 0
            s = 0
        t.append(number)
        t.append(x)
        t.append(y)
        t.append(tl)
        t.append(tr)
        t.append(q)
        t.append(s)
        data.append(t)
    file_name = '..\\data\\data' + str(I) + '.csv'
    header = ['number','x','y','tl','tr','q','s']
    with open(file_name,'w',encoding = 'utf-8',newline='') as file:
        writer = csv.writer(file)
        # writer.writerow(header)
        for p in data:
            writer.writerow(p)
for i in range(0,50):
    gen(i)