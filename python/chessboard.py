# -*- coding: utf-8 -*-
import random

print '''
          本程序以棋盘左侧为坐标原点，
          请根据提示依次输入起始坐标值x、y,
          然后输入终点坐标值N .
          要求x,y,N的值不能小于0，并且不得大于8.
          开始输入·····
      '''

#此处可简化
up_to_right_up = (1, 2)
up_to_left_up = (-1, 2)
down_to_right_down = (1, -2)
down_to_left_down = (-1, -2)
left_to_left_up = (-2, 1)
left_to_left_down = (-2, -1)
right_to_right_up = (2, 1)
right_to_right_down = (2, -1)

actions = [
    up_to_right_up, up_to_left_up,
    down_to_right_down, down_to_left_down,
    left_to_left_up, left_to_left_down,
    right_to_right_up, right_to_right_down
]

i = 0
res = {}  # 记录随机产生的最短路径，以便使路径最短化


def action_method(start_point, end_point, key, paths, actions):
    if start_point == end_point:
        print '已经在原来位置'
    num = random.randint(0, 7)
    method = actions[num]
    x = start_point[0] + method[0]
    y = start_point[1] + method[1]
    if x > 0 and x < 9 and y > 0 and y < 9:
        new_start = (x, y)
        paths.append(new_start)
        if new_start == end_point:
            if key[0] in paths:
                paths = paths[paths.index(key[0]) + 1:]
            if key in res.keys():
                if len(paths) < len(res[key]):
                    res[key] = paths
            else:
                res[key] = paths

            for path_point in res[key]:
                print path_point
            print '到达目标'
        else:
            action_method(new_start, end_point, key, paths, actions)
    else:
        action_method(start_point, end_point, key, paths, actions)


def start():
    x = int(input('请输入x：'))
    y = int(input('请输入y：'))
    N = int(input('请输入N：'))
    #TODO 对输入内容进行限定
    start_point = (x, y)
    end_point = (N, N)
    key = (start_point, end_point)
    print '起始坐标%s;\n终点坐标%s' % key
    paths = []
    action_method(start_point, end_point, key, paths, actions)
    

def end():
    return True


def main():
    print """ 输入S开始，输入E结束"""
    a = raw_input('请输入:')
    if a == 'S':
        start()
        main()
    elif a == 'E':
        end()
    else:
        main()


if __name__ == "__main__":
    main()


