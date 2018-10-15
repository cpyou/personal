d1 = []
d2 = []
count = 1000
for i in range(count):
    d1.append({
        'id': i,
        'name': 'name_{}'.format(i)
    })

for i in range(count):
    d2.append({
        'd1_id': i,
        'remark': 'remark_{}'.format(i)
    })

@profile
def bl1():
    res1 = []
    for item in d1:
        f_data = list(filter(lambda x: x['d1_id'] == item['id'], d2))
        if f_data:
            remark = f_data[0]['remark']
        else:
            remark = ''
        res1.append({
            'id': item['id'],
            'name': item['name'],
            'remark': remark
        })
    return res1

@profile
def bl2():
    res2 = []
    tamp = {}
    for item in d2:
        tamp[item['d1_id']] = item
    for item in d1:
        res2.append({
            'id': item['id'],
            'name': item['name'],
            'remark': tamp[item['id']]['remark']
        })
    return res2
res1 = bl1()
res2 = bl2()
if res1 == res2:
    print('结果一致')
