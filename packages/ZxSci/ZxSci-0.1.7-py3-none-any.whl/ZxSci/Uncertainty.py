from decimal import Decimal


def CalUncer(data_list):
    data_num = len(data_list)
    data_sum = sum(data_list)
    data_Average = Decimal(str(data_sum)) / Decimal(str(data_num))
    L2_sum = Decimal('0')
    for data in data_list:
        L2_sum += (Decimal(str(data)) - data_Average) ** Decimal('2')
    Ua = (L2_sum / (data_num * data_num - Decimal('1'))) ** Decimal('0.5')
    E = Ua / data_Average
    print("+--------------------------------------+")
    print("|  平均值是:     \t{:^12.6f}       |".format(data_Average))
    print("|  A类不确定度是: \t{:^12.6f}       |".format(Ua))
    print("|  相对不确定度是: \t{:^12.6f}%      |".format(E * Decimal('100')))
    print("+--------------------------------------+")
