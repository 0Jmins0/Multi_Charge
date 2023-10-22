import random
from readData import readmain
from LNS_SPP import LNS
from LNS_SPP import get_init_sol
from feasiblity import check

def main(k,instance):
    init_sol,init_cost = LNS(instance)
    select_bank = check(init_sol,instance)
    print(select_bank)
    return init_sol,init_cost


def evaluate(a,k):
    random.seed(k)
    num, x, y, tl, tr, q ,s= readmain(a)
    instance = {} # 定义问题设定字典
    instance['num'] = int(num) # 客户点数
    instance['x'] = x # 每个客户的经度
    instance['y'] = y # 每个客户的纬度
    instance['tl'] = tl # 每个客户的时间窗左端
    instance['tr'] = tr # 每个客户的时间窗右端
    instance['q'] = q # 每个客户的货物载量
    instance['s'] = s #每个客户的服务时间 (数据保证了 tr - tl >= s)
    # print(instance['x'][0] + 1)
    return main(k,instance)