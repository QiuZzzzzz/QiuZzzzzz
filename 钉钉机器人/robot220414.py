import requests
import json
import time
import hmac
import hashlib
import base64
import urllib.parse
import datetime
from django.http import HttpResponse, JsonResponse
import gettoken
import pathlib
import lightmeal


def getsign():
    timestamp = str(round(time.time() * 1000))
    secret = 'ZN4yoH2'
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    url = "&timestamp=%s&sign=%s" % (timestamp, sign)
    return url


def getnew():
    url = "http://open.iciba.com/dsapi/"
    r = requests.get(url)
    content = r.json()['content']
    note = r.json()['note']
    fenxiang_img = r.json()['fenxiang_img']
    return content, note, fenxiang_img


''' 发送文本消息
    headers = {
            'Content-Type': 'application/json'
        }
    if start_time>=now_time:
        data = {"msgtype": "text", "text": {"content": "—————————华丽的分割线—————————\n\r 午餐报名TEST，需要的请@小G。"}, "at": {"isAtAll": False}}
    else:
        data = {"msgtype": "text", "text": {"content": "—————————华丽的分割线—————————\n\r 晚餐报名TEST，需要的请@小G。"}, "at": {"isAtAll": False}}
    #print(data)
    response = requests.post(url, json=data, headers=headers)
'''


# 发送markdown
def sendmessage():
    url = "https://oapi.dingtalk.com/robot/send?access_token=931407289%s" % getsign()
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": 'ceshi',
            "text": 'ceshi'
        },

        "at": {
            "atUserIds": [
                '15954682306537057'
            ],
        }
    }
    # 利用requests发送post请求
    if gettoken.getrest() == 'N':
        req = requests.post(url, json=data)


#      "\n>*[小G使用说明](http://101.34.216.8:8088/%E5%B0%8FG%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E.html)*\n>"
def send_md_msg():
    start_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '11:50', '%Y-%m-%d%H:%M')
    end_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '13:29', '%Y-%m-%d%H:%M')
    # 当前时间
    now_time = datetime.datetime.now()
    url = "https://oapi.dingtalk.com/robot/send?access_token=93140720faa22589%s" % getsign()
    userid = '15954682306537057'
    title = '点餐啦！'
    if start_time >= now_time:
        data1 = "\n # **午餐报名** \n"
    else:
        data1 = "\n # **晚餐报名** \n"
    # message=" @" + userid + "  \n  " +"# 一级标题  \n  " +"## 二级标题  \n  " +"### 三级标题  \n  " +"#### 四级标题  \n  " +"##### 五级标题  \n  " +"###### 六级标题  \n  "
    message = "![screenshot](" + getnew()[
        2] + ")" + data1 + "  \n  " + "[点击这里或者@小G回复1点餐](dtmd://dingtalkclient/sendMessage?content=1)\n" + "\n & \n" + "[点击这里或者@小G回复2预定明天中午轻食](dtmd://dingtalkclient/sendMessage?content=2)\n"
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": title,
            "text": message
        },
        '''
        "msgtype": "text",
        "text": {
            "content": message
        },
        '''
        "at": {
            "atUserIds": [
                userid
            ],
        }
    }
    # 利用requests发送post请求
    if gettoken.getrest() == 'N':

        # print(req.text)
        # 生成txt并插入数据
        # start_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '11:50', '%Y-%m-%d%H:%M')

        # now_time = datetime.datetime.now()
        if now_time <= start_time:
            txtname = './peoplemessage/' + str(datetime.datetime.now().date().year) + str(
                datetime.datetime.now().date().month) + str(datetime.datetime.now().date().day) + '01'
            txtname2 = './peoplemessage/' + str(datetime.datetime.now().date().year) + str(
                datetime.datetime.now().date().month) + str(datetime.datetime.now().date().day) + '012'
            file_handle = open(txtname + '.txt', mode='a')
            file_handle.close()
            file_handle = open(txtname2 + '.txt', mode='a')
            file_handle.close()
            file_handle2 = open('./peoplemessage/订阅午餐.txt', mode='r+')
            file_handle3 = open('./peoplemessage/订阅轻食.txt', mode='r+')
            contentss = str(file_handle2.read())
            contentss3 = str(file_handle3.read())
            file_handle2.close()
            file_handle3.close()
            file_handle = open(txtname + '.txt', mode='a+')
            contents = str(file_handle.read())
            if contentss not in contents:
                file_handle.write(contentss)
            file_handle.close()
            file_handle = open(txtname2 + '.txt', mode='a+')
            contents3 = str(file_handle.read())
            if contentss3 not in contents3:
                file_handle.write(contentss3)
            file_handle.close()
        else:
            txtname = './peoplemessage/' + str(datetime.datetime.now().date().year) + str(
                datetime.datetime.now().date().month) + str(datetime.datetime.now().date().day) + '02'
            file_handle = open(txtname + '.txt', mode='a')
            file_handle.close()
            file_handle2 = open('./peoplemessage/订阅晚餐.txt', mode='r+')
            contentss = str(file_handle2.read())
            file_handle2.close()
            file_handle = open(txtname + '.txt', mode='a+')
            contents = str(file_handle.read())
            # print(contentss)
            if contentss not in contents:
                file_handle.write(contentss)
            file_handle.close()
        req = requests.post(url, json=data)


def send_statistic():
    import DingRobot
    start_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '11:50', '%Y-%m-%d%H:%M')
    end_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '13:29', '%Y-%m-%d%H:%M')
    # 当前时间
    now_time = datetime.datetime.now()
    if gettoken.getrest() == 'N':
        txtname = DingRobot.timetxt()[0]
        txtname2 = DingRobot.timetxt()[1]
        url = "https://oapi.dingtalk.com/robot/send?access_token=9314072%s" % getsign()

        if pathlib.Path(txtname + '.txt').exists() and pathlib.Path(txtname2 + '.txt').exists():
            file_handle = open(txtname + '.txt').read()
            f = str(file_handle.count('，'))

            file_handle = open(txtname + '.txt', mode='r')
            contents = str(file_handle.read())
            file_handle.close()
            # 请示
            file_handle = open(txtname2 + '.txt').read()
            g = str(file_handle.count('，'))

            file_handle = open(txtname2 + '.txt', mode='r')
            contents2 = str(file_handle.read())
            file_handle.close()
            # 前一日轻食
            txtname3 = lightmeal.getrest()
            file_handle = open(txtname3 + '.txt').read()
            h = str(file_handle.count('，'))

            file_handle = open(txtname3 + '.txt', mode='r')
            contents3 = str(file_handle.read())
            file_handle.close()
            if now_time < end_time:
                text = '数字化中心今日轻食' + h + '份:' + contents3 + '\n &\n' + '数字化中心常规餐' + f + '份:' + contents + '\n &\n' + '数字化中心来日轻食已预定' + g + '份:' + contents2
            else:
                text = '数字化中心常规餐' + f + '份:' + contents + '\n &\n' + '数字化中心来日轻食已预定' + g + '份:' + contents2
        elif pathlib.Path(txtname + '.txt').exists() and pathlib.Path(txtname2 + '.txt').exists() == False:
            file_handle = open(txtname + '.txt').read()
            f = str(file_handle.count('，'))

            file_handle = open(txtname + '.txt', mode='r')
            contents = str(file_handle.read())
            file_handle.close()
            text = '数字化中心常规餐' + f + '份:' + contents
        elif pathlib.Path(txtname + '.txt').exists() == False and pathlib.Path(txtname2 + '.txt').exists():
            file_handle = open(txtname2 + '.txt', mode='r')
            g = str(file_handle.count('，'))
            contents2 = str(file_handle.read())
            file_handle.close()
            text = '数字化中心轻食已预定' + g + '份:' + contents2
        else:
            text = '数字化中心无人点餐'
        headers = {
            'Content-Type': 'application/json'
        }
        userid = "0138002165941018"
        data = {"msgtype": "text", "text": {"content": text}, "at": {"atUserIds": [userid], }}

        response = requests.post(url, json=data, headers=headers)
        # 0138002165941018

        data = {"msgtype": "text", "text": {"content": "点餐结束"}, "at": {"isAtAll": False}}
        response = requests.post(url, json=data, headers=headers)
        # req = requests.post(url, json=data)


if __name__ == "__main__":
    send_md_msg()
    # send_statistic()
