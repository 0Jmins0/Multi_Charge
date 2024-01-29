import random
from read_data import Read_Data
from LNS_SPP import LNS
from feasiblity import check
from draw import Draw
def main(instance):
    # 获得送货车路线池
    init_sol,init_cost ,Dis_List,time_window= LNS(instance)
    print("init_sol:",init_sol)
    print("time_window:",time_window)

    # 获得充电车选择的充电点
    select_bank = check(init_sol,instance,Dis_List,time_window)
    print("charge node:",select_bank)
    #
    # # 可视化
    Draw(instance,init_sol,select_bank,time_window,Dis_List)

    # return select_bank

def evaluate(a,k):
    random.seed(k)
    instance= Read_Data(a)
    return main(instance)