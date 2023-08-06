from decimal import Decimal


def AveDevCalTab(xlist, ylist):
    x_list = []
    y_list = []
    for x in xlist:
        x_list.append(Decimal(str(x)))
    for y in ylist:
        y_list.append(Decimal(str(y)))
    DEV = []
    DEV.append(y_list)
    N = len(x_list)
    for jie in range(1, N):
        n = len(DEV[jie - 1])
        dev = []
        for i in range(n):
            if (i < jie):
                dev.append(Decimal('0'))
            else:
                ave_dev = (DEV[jie - 1][i] - DEV[jie - 1][i - 1]) / (x_list[i] - x_list[i - jie])
                dev.append(ave_dev)
        DEV.append(dev)
    print("均差计算表如下:")
    print("|{:^12}|{:^12}".format("X", "Y"), end="|")
    for i in range(1, N):
        print("{:^12}|".format("N" + str(i)), end="")
    print("")
    for i in range(N):
        print("|", end="")
        print("{:^12.5f}".format(x_list[i]), end="|")
        for j in range(N):
            if (i < j):
                print("{:^12}".format(""), end="|")
            else:
                print("{:^12.5f}".format(DEV[j][i]), end="|")
        print("")


def NewtonChaZhi(xlist, ylist, x_in):
    x_list = []
    y_list = []
    x = Decimal(str(x_in))
    for x in xlist:
        x_list.append(Decimal(str(x)))
    for y in ylist:
        y_list.append(Decimal(str(y)))
    DEV = []
    DEV.append(y_list)
    N = len(x_list)
    for jie in range(1, N):
        n = len(DEV[jie - 1])
        dev = []
        for i in range(n):
            if (i < jie):
                dev.append(Decimal('0'))
            else:
                ave_dev = (DEV[jie - 1][i] - DEV[jie - 1][i - 1]) / (x_list[i] - x_list[i - jie])
                dev.append(ave_dev)
        DEV.append(dev)
    y = Decimal('0')
    for i in range(N):
        a = DEV[i][i]
        p = Decimal('1')
        for j in range(i):
            p *= (Decimal(str(x)) - x_list[j])
        y += a * p
    return y


def DiffTable(xlist, ylist):
    x_list = []
    y_list = []
    for x0 in xlist:
        x_list.append(Decimal(str(x0)))
    for y0 in ylist:
        y_list.append(Decimal(str(y0)))
    h = x_list[1] - x_list[0]
    flag = 1
    for i in range(len(x_list) - 1):
        if (x_list[i + 1] - x_list[i] - h != 0):
            flag = 0
            break
    if (flag == 0):
        print("输入的x不是等差的")
        return -1
    else:
        dif_mat = []
        dif_mat.append(y_list)
        N = len(x_list)
        for jie in range(1, N):
            n = len(dif_mat[jie - 1])
            dev = []
            for i in range(n):
                if (i < jie):
                    dev.append(0)
                else:
                    ave_dev = (dif_mat[jie - 1][i] - dif_mat[jie - 1][i - 1])
                    dev.append(ave_dev)
            dif_mat.append(dev)
        print("差分计算表如下:")
        print("|{:^12}|{:^12}".format("X", "Y"), end="|")
        for i in range(1, N):
            print("{:^12}|".format("f^" + str(i)), end="")
        print("")
        for i in range(N):
            print("|", end="")
            print("{:^12.5f}".format(x_list[i]), end="|")
            for j in range(N):
                if (i < j):
                    print("{:^12}".format(""), end="|")
                else:
                    print("{:^12.5f}".format(dif_mat[j][i]), end="|")
            print("")


def NewtonQianCha(xlist, ylist, x_in):
    x_list = []
    y_list = []
    x = Decimal(str(x_in))
    for x0 in xlist:
        x_list.append(Decimal(str(x0)))
    for y0 in ylist:
        y_list.append(Decimal(str(y0)))
    h = x_list[1] - x_list[0]
    flag = 1
    for i in range(len(x_list) - 1):
        if (x_list[i + 1] - x_list[i] - h != 0):
            flag = 0
            break
    if (flag == 0):
        print("输入的x不是等差的")
        return -1
    else:
        dif_mat = []
        dif_mat.append(y_list)
        N = len(x_list)
        for jie in range(1, N):
            n = len(dif_mat[jie - 1])
            dev = []
            for i in range(n):
                if (i < jie):
                    dev.append(0)
                else:
                    ave_dev = (dif_mat[jie - 1][i] - dif_mat[jie - 1][i - 1])
                    dev.append(ave_dev)
            dif_mat.append(dev)
        y = dif_mat[0][0]
        t = (Decimal(str(x)) - x_list[0]) / h
        for jieshu in range(1, N):
            a = dif_mat[jieshu][jieshu]
            p = Decimal('1')
            jiecheng_shu = Decimal('1')
            for x in range(jieshu):
                jiecheng_shu *= Decimal(str(x + 1))
            for j in range(jieshu):
                p *= (t - Decimal(str(j)))
            y += a * p / jiecheng_shu
        return y
