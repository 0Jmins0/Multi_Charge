import matplotlib.pyplot as plt
import global_parameter as gp

Delivery_Capacity = gp.Delivery_Capacity # 送货车最大载货量
Battery_Capacity = gp.Battery_Capacity # 送货车电池容量
Delivery_Cost = gp.Delivery_Cost # 每辆送货车的价格
P_Dis_Charge = gp.P_Dis_Charge # 距离和电量的系数，距离乘以系数为耗电量
P_Charge_Cost = gp.P_Charge_Cost # 耗电量和花费的系数，耗电量乘以系数为花费
P_Delivery_Speed = gp.P_Delivery_Speed # 送货车距离和时间的系数，距离乘以系数为时间
P_Charge_Speed = gp.P_Charge_Speed # 充电车距离和时间的系数，距离乘以系数为时间
def Draw(instance,route_pool,charge_node,time_window,Dis_List):
    # 获取Matplotlib默认的颜色循环
    color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']

    N = instance['N']

    X = instance['x']
    Y = instance['y']
    tl = instance['tl']
    tr = instance['tr']
    # 设置图像大小
    # plt.figure(figsize=(3,3))
    plt.scatter(X[1:-1],Y[1:-1])
    plt.scatter(X[0], Y[0], marker='*', color='red', s=200, label='Star Point')

    # for i, (x, y) in enumerate(zip(X[:-1], Y[:-1])):
    #     plt.annotate(f"{i}: ({x}, {y})", (x, y), textcoords="offset points", xytext=(1, 1), ha='right')

    number = 0
    for route in route_pool:
        Len = len(route)
        for i in range(0,Len - 1):
            x1 = X[route[i]]
            x2 = X[route[i + 1]]
            y1 = Y[route[i]]
            y2 = Y[route[i + 1]]
            plt.plot([x1, x2], [y1, y2], color=color_cycle[number])
            x_mid = (x1 + x2) / 2
            y_mid = (y1 + y2) / 2
            distance = round(Dis_List[route[i]][route[i + 1]][2] * P_Delivery_Speed)
            plt.annotate(f"time {route[i]}-{route[i + 1]}: {distance:.2f}", (x_mid, y_mid), textcoords="offset points",
                         xytext=(0, 5), ha='center')
            if(i != 0):
                plt.scatter(x1, y1, color = 'blue',s = 100, marker='o')
                plt.annotate(f"{route[i]}: ({time_window[number][i][0]}, {time_window[number][i][1]})", \
                             xy = (x1, y1), textcoords="offset points", xytext=(1, 1), ha='right')
        number = number + 1
    for node in charge_node:
         plt.scatter(X[node], Y[node], s=100,color = 'yellow', marker='o')
    # plt.xlim(-180, 180)
    # plt.ylim(-180, 180)
    plt.show()