# -*- coding: utf-8 -*-
import random

print '''
          本程序以棋盘左侧为坐标原点，
          请根据提示依次输入起始坐标值x、y,
          然后输入终点坐标值N .
          要求x,y,N的值不能小于0，并且不得大于8.
          开始输入·····
      '''

x = int(input('请输入x：'))
y = int(input('请输入y：'))
N = int(input('请输入N：'))
#TODO 对输入内容进行限定
start = (x, y)
end = (N, N)
print '起始坐标%s;\n终点坐标%s' % (start, end)

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


def action_method(start, end, actions):
    if start == end:
        print '已经在原来位置'
        return True
    num = random.randint(0, 7)
    method = actions[num]
    x = start[0] + method[0]
    y = start[1] + method[1]
    if x > 0 and x < 9 and y > 0 and y < 9:
        new_start = (x, y)
        print new_start
        if new_start == end:
            print '到达目标'
            return True
        else:
            action_method(new_start, end, actions)
    else:
        action_method(start, end, actions)

action_method(start, end, actions)
