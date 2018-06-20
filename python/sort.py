a = [1, 5, 2, 11, 3, 24, 5, 5, 7, 3, 2, 6, 10, 0]
print a
for i in range(len(a) -1):
    for j in range(i + 1, len(a)):
        if (a[i] > a[j]):
            tmp = a[i]
            a[i] = a[j]
            a[j] = tmp
    print a

