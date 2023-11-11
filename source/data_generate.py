import csv
import random
import numpy as  np

def gen(I):
    n = random.randint(10,100)
    data = []
    # 0,n + 1 : 仓库，[1,n] : 用户
    for i in range(0, n + 2):
        t = []
        # 编号
        number = i
        # 坐标
        x = np.random.randint(0, 360)
        y = np.random.randint(-180, 180)
        # 服务时间
        s = np.random.randint(10,30)
        # 时间窗
        tl = np.random.randint(0, 840 - s)
        tr = np.random.randint(tl + s, 840)
        # 载货量
        q = np.random.randint(10, 100)
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
    header = ['num','x','y','tl','tr','q','s']
    with open(file_name,'w',encoding = 'utf-8',newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for p in data:
            writer.writerow(p)
for i in range(0,50):
    gen(i)