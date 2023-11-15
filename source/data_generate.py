import csv
import math
import random
import numpy as  np
import global_parameter as gp

Delivery_Capacity = gp.Delivery_Capacity # 送货车最大载货量
Battery_Capacity = gp.Battery_Capacity # 送货车电池容量
Delivery_Cost = gp.Delivery_Cost # 每辆送货车的价格
P_Dis_Charge = gp.P_Dis_Charge # 距离和电量的系数，距离乘以系数为耗电量
P_Charge_Cost = gp.P_Charge_Cost # 耗电量和花费的系数，耗电量乘以系数为花费
P_Delivery_Speed = gp.P_Delivery_Speed # 送货车距离和时间的系数，距离乘以系数为时间
P_Charge_Speed = gp.P_Charge_Speed # 充电车距离和时间的系数，距离乘以系数为时间

# 检查任意两点是否可以满电量可达
def Get_Dis_OK(x1,y1,x2,y2):
    p1 = x1 - x2
    p2 = y1 - y2
    dis = round(math.sqrt(p1 * p1 + p2 * p2))
    if(round(dis * P_Dis_Charge) <= Battery_Capacity):
        return 1
    else:
        return 0

def Get_Time_OK(x1,y1,x2,y2,tl,tr,s):
    p1 = x1 - x2
    p2 = y1 - y2
    dis = round(math.sqrt(p1 * p1 + p2 * p2))
    time = dis * P_Delivery_Speed
    early_big = max(time,tl)
    early_end = early_big + s
    if(early_end + time <= 840):
        return 1
    else:
        return 0

def gen(I):
    n = random.randint(10,50)
    n = 6
    data = []
    # 0,n + 1 : 仓库，[1,n] : 用户
    for i in range(0, n + 2):
        t = []
        # 编号
        number = i
        ok = 0
        while(ok == 0):
            ok = 1
            # 坐标
            x = np.random.randint(-180, 180)
            y = np.random.randint(-180, 180)
            for j in range(0,i):
                ok = ok & Get_Dis_OK(data[j][1],data[j][2],x,y)


        # 服务时间
        s = np.random.randint(10,30)
        ok = 0
        while (ok == 0 and i != 0 and i != n + 1):
            # 时间窗
            tl = np.random.randint(0, 840 - s)
            tr = np.random.randint(tl + s, 840)
            if(Get_Time_OK(data[0][1],data[0][2],x,y,tl,tr,s)):
                ok = 1
        # 载货量
        q = np.random.randint(10, 100)
        # 如果是仓库
        if(i == 0):
            tl = 0
            tr = 840
            q = 0
            s = 0
        if(i == n + 1):
            x = data[0][1]
            y = data[0][2]
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
        # print(t)
    file_name = '..\\data\\data' + str(I) + '.csv'
    header = ['num','x','y','tl','tr','q','s']
    with open(file_name,'w',encoding = 'utf-8',newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for p in data:
            writer.writerow(p)
# for i in range(1,51):
#     gen(i)
gen(0)