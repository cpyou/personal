a = [1, 5, 2, 11, 3, 24, 5, 5, 7, 3, 2, 6, 10, 0]
print a
# 冒泡排序
for i in range(len(a) - 1):
    for j in range(len(a) -i -1):
        if a[j ] > a[j +1]:
            tmp = a[j]
            a[j] = a[j + 1]
            a[j +1] = tmp
   # if endsort == 0:
   #     break
    print a

