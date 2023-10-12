import random
from readData import readmain
from LNS_SPP import LNS
from LNS_SPP import get_init_sol

def main(k,instance):
    init_sol,init_cost = LNS(instance)
    return init_sol,init_cost


def evaluate(a,k):
    random.seed(k)
    num, x, y, tl, tr, q ,s= readmain(a)
    instance = {}
    instance['num'] = int(num)
    instance['x'] = x
    instance['y'] = y
    instance['tl'] = tl
    instance['tr'] = tr
    instance['q'] = q
    instance['s'] = s
    # print(instance['x'][0] + 1)
    return main(k,instance)