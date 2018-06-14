def fact1(n):
    s = 0
    temp = 1
    for i in range(1, n + 1):
        temp *= i
        s += temp
    print s
    return s

def fact2(n):
    return n 

fact1(1)
fact1(2)
fact1(3)
fact1(4)
