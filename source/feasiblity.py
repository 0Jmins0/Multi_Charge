import math
import random
import copy
import global_parameter as gp
import numpy as np
import LNS_SPP as LS

from LNS_SPP import Dis_List
from LNS_SPP import instance

Delivery_Capacity = gp.Delivery_Capacity # 送货车最大载货量
Battery_Capacity = gp.Battery_Capacity # 送货车电池容量
Delivery_Cost = gp.Delivery_Cost # 每辆送货车的价格
P_Dis_Charge = gp.P_Dis_Charge # 距离和电量的系数，距离乘以系数为耗电量
P_Charge_Cost = gp.P_Charge_Cost # 耗电量和花费的系数，耗电量乘以系数为花费
P_Delivery_Speed = gp.P_Delivery_Speed # 送货车距离和时间的系数，距离乘以系数为时间
P_Charge_Speed = gp.P_Charge_Speed # 充电车距离和时间的系数，距离乘以系数为时间


def check(route_pool): #DP部分
    N = instance['N']
    # 初始化
    dp = np.zeros((N, Battery_Capacity, Battery_Capacity, 4)).tolist()
    for i in range(0,N + 2):
        for j in range(0,Battery_Capacity + 1):
            for k in range(0,Battery_Capacity + 1):
                dp[i][j][k][0] = float('inf')
                dp[i][j][k][1] = -1
                dp[i][j][k][2] = -1
                dp[i][j][k][3] = 0
    for i in range(0,4):
        dp[0][Battery_Capacity][0][i] = 0

    # 转移
    for i in range(1,N + 2):
        cus = LS.Get_Distance(i,i - 1) * P_Dis_Charge
        for j in range(0,Battery_Capacity + 1):
            for k in range(0,Battery_Capacity - j + 1):
                for kk in range(0,j + cus + 1):
                    # 不充电
                    # j - kk + cus >= 0
                    # j + k <= Battery_Capacity
                    p = dp[i - 1][j - kk + cus][kk][1]
                    if (dp[i][j][0][0] > dp[i - 1][j - kk + cus][kk][0]):
                        dp[i][j][0][0] = dp[i - 1][j - kk + cus][kk][0]
                        dp[i][j][0][1] = p
                        dp[i][j][0][2] = p
                        dp[i][j][0][3] = kk

                    # 充电
                    if (dp[i][j][k][0] > dp[i - 1][j - kk + cus][kk][0] + (LS.Get_Distance(i,p) * P_Dis_Charge + k) * P_Charge_Cost):
                        dp[i][j][k][0] = dp[i - 1][j - kk + cus][kk][0] + (LS.Get_Distance(i,p) * P_Dis_Charge + k) * P_Charge_Cost
                        dp[i][j][k][1] = i
                        dp[i][j][k][2] = p
                        dp[i][j][k][3] = kk
    ans = 0
    J = K = KK = now = pre = 0
    for j in range(0,Battery_Capacity + 1):
        for k in range(0,Battery_Capacity - j + 1):
            if(ans < dp[N +1][j][k][0]):
                ans = dp[N + 1][j][k][0]
                J = j
                K = k
    now = dp[N + 1][J][K][1]
    pre = dp[N + 1][J][K][2]
    KK = dp[N + 1][J][K][3]

    ANS = []
    if (now == N + 1):
        ANS.append(N + 1)
    now = N + 1
    while (pre != 0):
        ANS.append(pre)
        cus = LS.Get_Distance(now, pre) * P_Dis_Charge
        J = J + cus - KK  # pre 点对应的剩余电量
        K = KK  # pre 点对应的充电量
        now = pre
        pre = dp[now][J][K][2]  # pre 的前一个点
        KK = dp[now][J][K][3]  # pre 前一个点对应的充电量

    return ANS