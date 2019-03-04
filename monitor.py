# -*- coding: utf-8 -*-
#@author: limeng
#@file: monitor.py
#@time: 2019/2/23 20:49
"""
文件说明：微信和电脑交互
"""
import itchat
import os
import time
from PIL import ImageGrab #用于将当前屏幕的内容或者剪贴板上的内容拷贝到PIL图像内存

sendMsg = "{消息助手}暂时无法回复"
usageMsg = "回复1 截图，\n"\
    "回复2 电脑锁屏 \n"\
    "回复3 执行文件 \n"\
    "回复{退出QQ} 或 {退出微信} 可同时退出两个应用 \n"\
    "回复{exit} 退出程序 \n"\
    "回复{管萍} 有惊喜\n"
flag = 0#消息助手开关
run_flag = 0 #脚本运行开关
nowTime = time.localtime()
filename = "log.txt"

myfile = open(filename,"w")

@itchat.msg_register("Text")
def text_reply(msg):
    print(msg)
    global run_flag
    message = msg["Content"]
    fromName = msg["FromUserName"]
    toName = msg["ToUserName"]

    if toName == "filehelper":
        if run_flag == 0:
            if message == "1":
                #电脑屏幕截图
                screen = ImageGrab.grab()
                screen.save("./screenShot.png","png")
                itchat.send("@img@%s"%u"screenShot.png",toName)
            elif message == "2":
                os.system("rundll32.exe user32.dll LockWorkStation")#锁屏
            elif message == "3":
                run_flag = 1
                itchat.send("当前路径为{}".format(os.getcwd()), toName)
                itchat.send("请输入当前路径中的文件名或者重新输入文件路径", toName)
                itchat.send("回复{返回} 返回主页\n 回复{查看} 查看当前路径下所有文件\n", toName)
            elif message == "退出QQ" or message == "退出微信":
                os.system("taskkill /im QQ.exe /f")
                os.system("taskkill /im WeChat.exe /f")
                itchat.send("QQ和微信已退出", toName)
            elif message == "exit":
                itchat.send("此功能开发中。。。", toName)
                os.system("taskkill /im QQ.exe /f")
            elif message == "管萍":
                itchat.send("管萍是一只可爱的小猪", toName)
            else:
                itchat.send("听不懂你在说什么哦", toName)
        else:
            if message == "返回":
                run_flag = 0
                itchat.send(usageMsg, toName)
            elif message == "查看":
                files = str(os.listdir(os.getcwd()))
                itchat.send(files, toName)
            else:
                try:
                    os.startfile(message)
                    itchat.send(message+"已执行", toName)
                    itchat.send(usageMsg, toName)
                    run_flag = 0
                except:
                    itchat.send("路径错误，请重新输入", toName)

    elif flag == 1:
        itchat.send(sendMsg,fromName)
        myfile.write(str(nowTime.tm_mday)+str(nowTime.tm_hour)+str(nowTime.tm_min))
        myfile.write(message)
        myfile.write("\n")
        myfile.flush()

if __name__ == '__main__':
    itchat.auto_login()
    itchat.send(usageMsg,"filehelper")
    itchat.run()

