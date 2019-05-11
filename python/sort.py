a = [1, 5, 2, 11, 3, 24, 5, 5, 7, 3, 2, 6, 10, 0]
print(a)
# 冒泡排序
def bubble_sort(data):
    for i in range(len(a) - 1):
        for j in range(len(a) -i -1):
            if a[j ] > a[j +1]:
                tmp = a[j]
                a[j] = a[j + 1]
                a[j +1] = tmp
    print(data)
    return data


def quick_sort(data):
    if len(data) >= 2:
        mid = data[len(data)//2]
        left, right = [], []
        data.remove(mid)
        for num in data:
            if num >= mid:
                right.append(num)
            else:
                left.append(num)
        result = quick_sort(left) + [mid] + quick_sort(right)
        print(result)
        return result
    else:
        return data


# bubble_sort(a)
quick_sort(a)
