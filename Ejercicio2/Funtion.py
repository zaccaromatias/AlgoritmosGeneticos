
def GetValue(item):
    sumvallocal = 0
    for t in range(len(item)):
        sumvallocal += item[t].price
    return sumvallocal

def GetVolumen(item):
    sumsumlocal = 0
    for t in range(len(item)):
        sumsumlocal += item[t].volumen
    return sumsumlocal