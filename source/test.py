import random
from read_data import Read_Data
from LNS_SPP import LNS
from feasiblity import check,check_with_regular_time,check_with_timewindow
from draw import Draw,Draw2
def main(instance):
    # 获得送货车路线池
    init_sol,init_cost ,Dis_List,time_window= LNS(instance)
    print("init_sol:",init_sol)
    print("time_window:",time_window)

    # 获得充电车选择的充电点
    # select_bank = check(init_sol,instance,Dis_List,time_window)

    init_sol = [[0, 25, 13, 27, 8, 7, 5, 2, 10, 18, 15, 16, 38]]
    time_window = [[[0, 290], [10, 300], [198, 329], [262, 350], [280, 368], [308, 396], [335, 423], [352, 474], [455, 501], [478, 754], [741, 790], [758, 824], [822, 840]]]

    select_bank = check_with_timewindow(init_sol, instance, Dis_List, time_window)

    print("charge node_time_window:", select_bank)
    # init_sol = [[0,1,2,3,4,5]]

    select_bank = check_with_regular_time(init_sol, instance, Dis_List, time_window)

    print("charge node_regular_time:",select_bank)
    #
    # # 可视化
    # Draw(instance,init_sol,select_bank,time_window,Dis_List)

    Draw2(instance, init_sol, select_bank, time_window, Dis_List)
    # return select_bank

def evaluate(a,k):
    random.seed(k)
    instance= Read_Data(a)
    return main(instance)