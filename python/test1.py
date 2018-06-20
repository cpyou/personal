#! /usr/bin/env python
#coding=utf-8
#提取QQ群成员
#by bugscaner
#email：bugscaner@qq.com
#http://tools.bugscaner.com

import re
import sys
import uiautomation as automation
reload(sys)
sys.setdefaultencoding('utf8')

#请打开QQ群聊天窗口,运行本程序即可
tencent = automation.WindowControl(ClassName="TXGuiFoundation")
for c,d in automation.WalkControl(tencent):
    if isinstance(c,automation.ListItemControl):
        #编码问题来个异常捕获
        try:
            print c.Name
        except:
            pass
