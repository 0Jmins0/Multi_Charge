import random
from read_data import Read_Data
from LNS_SPP import LNS
from feasiblity import check
from draw import Draw
def main(instance):
    init_sol,init_cost ,Dis_List,time_window= LNS(instance)
    print("init_sol:",init_sol)
    print("time_window:",time_window)
    select_bank = check(init_sol,instance,Dis_List)
    if(len(select_bank) == 0):
        print("This solution can't arrive")
    else:
        print("charge node:",select_bank)
    Draw(instance,init_sol,select_bank,time_window,Dis_List)
    return init_sol,init_cost

def evaluate(a,k):
    random.seed(k)
    N, instance= Read_Data(a)
    instance['N'] = N
    # print(instance.items())
    return main(instance)