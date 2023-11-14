import random
from read_data import Read_Data
from LNS_SPP import LNS

def main(instance):
    init_sol,init_cost = LNS(instance)
    # # select_bank = check(init_sol,instance)
    # print(select_bank)
    return init_sol,init_cost

def evaluate(a,k):
    random.seed(k)
    N, instance= Read_Data(a)
    instance['N'] = N
    print(instance.items())
    return main(instance)