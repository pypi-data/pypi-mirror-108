moude_dic = {1: "MathWork", 2: "showData", 3: "Uncertainty"}


def init():
    print("+" + "-" * 40 + "+")


def print_function(str, function_name, moude_id):
    print("|", end="")
    print(str)
    print("|", end="")
    print(function_name)
    print("|", end="")
    print("所属模块:\t" + moude_dic[moude_id])
    end()


def end():
    print("+" + "-" * 40 + "+")


init()
print_function("生产均差表:", "AveDevCalTab(xlist, ylist)", 1)
print_function("生产差分表:", "DiffTable(xlist, ylist)", 1)
print_function("牛顿差值多项式求值:", "NewtonChaZhi(xlist, ylist, x_in)", 1)
print_function("牛顿前插公式求值:", "NewtonQianCha(xlist, ylist, x_in)", 1)
print_function("绘制数据曲线:", "printData(x_list,y_list)", 2)
print_function("绘制多张数据曲线:", "printNpic()", 2)
print_function("计算不确定度:", "CalUncer(data_list)", 3)
