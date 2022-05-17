from flask import Flask, request
import hmac
import hashlib
import base64
import json
import requests
import time
import requests
import json
import time
import hmac
import hashlib
import base64
import urllib.parse
import datetime
from django.http import HttpResponse, JsonResponse
from flask import Flask, request, session, render_template, redirect, url_for
from flask import Flask
from urllib import parse
import hashlib
import base64, gzip
import colorama
import schedule
import os
import sys
from subprocess import Popen, PIPE, STDOUT
import pathlib
import lightmeal

app = Flask(__name__)


# print("Content-Type: text/html\n")

def timetxt():
    start_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '11:50', '%Y-%m-%d%H:%M')
    end_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '13:29', '%Y-%m-%d%H:%M')
    now_time = datetime.datetime.now()
    if now_time <= start_time:
        txtname = './peoplemessage/' + str(datetime.datetime.now().date().year) + str(
            datetime.datetime.now().date().month) + str(datetime.datetime.now().date().day) + '01'
        txtname2 = './peoplemessage/' + str(datetime.datetime.now().date().year) + str(
            datetime.datetime.now().date().month) + str(datetime.datetime.now().date().day) + '012'

    if now_time >= end_time:
        txtname = './peoplemessage/' + str(datetime.datetime.now().date().year) + str(
            datetime.datetime.now().date().month) + str(datetime.datetime.now().date().day) + '02'
        txtname2 = './peoplemessage/' + str(datetime.datetime.now().date().year) + str(
            datetime.datetime.now().date().month) + str(datetime.datetime.now().date().day) + '012'
    if now_time > start_time and now_time < end_time:
        txtname = './peoplemessage/' + str(datetime.datetime.now().date().year) + str(
            datetime.datetime.now().date().month) + str(datetime.datetime.now().date().day) + '03'
        txtname2 = './peoplemessage/' + str(datetime.datetime.now().date().year) + str(
            datetime.datetime.now().date().month) + str(datetime.datetime.now().date().day) + '012'
    return txtname, txtname2


def getnew():
    url = "http://open.iciba.com/dsapi/"
    r = requests.get(url)
    content = r.json()['content']
    note = r.json()['note']
    return content, note


# 消息数字签名计算核对
def check_sig(timestamp):
    app_secret = 'ZN4yoH2gwrjoIb3FCO0LdDu0_'
    app_secret_enc = app_secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, app_secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(app_secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = base64.b64encode(hmac_code).decode('utf-8')
    return sign


# 发送txt消息
def send_md_msg_text(senderid, message, webhook_url):
    data = {"msgtype": "text", "text": {"content": message}, "at": {"atUserIds": [senderid], "isAtAll": False}}
    # 利用requests发送post请求
    req = requests.post(webhook_url, json=data)


# 发送markdown消息
def send_md_msg(userid, title, message, webhook_url):
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
    req = requests.post(webhook_url, json=data)


# 处理自动回复消息
def handle_info(req_data):
    txtname = timetxt()[0]
    txtname2 = timetxt()[1]
    news = str(getnew())
    # 解析用户发送消息 通讯webhook_url 
    text_info = req_data['text']['content'].strip()
    webhook_url = req_data['sessionWebhook']
    senderid = req_data['senderStaffId']
    senderNick = req_data['senderNick']
    conversationTitle = req_data['conversationTitle']
    createAt = str(req_data['createAt'])
    # senderStaffId=req_data['senderStaffId']
    # print('***************text_info：', text_info)
    # 存储sendeNIck

    # 增加时间判断 220509
    start_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '10:50', '%Y-%m-%d%H:%M')
    end_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '13:29', '%Y-%m-%d%H:%M')
    end_time2 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '16:30', '%Y-%m-%d%H:%M')
    now_time = datetime.datetime.now()
    if text_info == "1":
        if now_time <= start_time or end_time <= now_time <= end_time2:

            file_handle = open(txtname + '.txt', mode='a')
            file_handle.close()
            file_handle = open(txtname + '.txt', mode='r+')
            contentss = str(file_handle.read())
            if senderNick in contentss:
                copy = senderNick + ",要再点一份吗?"
            else:
                file_handle.write(senderNick + '，')
                file_handle.close()
                file_handle = open(txtname + '.txt', mode='r+')
            contents = str(file_handle.read())
            file_handle.close()
            if senderNick in contentss:
                title = "点餐"
                text = copy + '\n\r' + """\n
    ![screenshot](https://staticedu-wps.cache.iciba.com/image/ea7edf9186d6a66b1439f6380d9ce964.jpg)\n>
    **[百度一下](https://www.baidu.com/)**\n>
                    """ + news + "\n"

            # 调用函数，发送markdown消息
            # send_md_msg( senderid,title,text, webhook_url)
        else:
            text = "请在规定时间内点餐,午餐10:50截止,晚餐16:30截止"
            send_md_msg_text(senderid, text, webhook_url)

    if text_info == "2":
        if now_time <= end_time2:
            file_handle = open(txtname2 + '.txt', mode='a')
            file_handle.close()
            file_handle = open(txtname2 + '.txt', mode='r+')
            contentss = str(file_handle.read())
            if senderNick not in contentss:
                file_handle.write(senderNick + '，')
            file_handle.close()
        else:
            text = "请在规定时间内点餐,午餐10:50截止,晚餐16:30截止"
            send_md_msg_text(senderid, text, webhook_url)

    if text_info == "11":
        file_handle = open(txtname + '.txt', mode='a+')
        file_handle.write(senderNick + '，')

        file_handle.close()

        text = senderNick + "，胃口不错哦" + "\n" + createAt
        # 调用函数，发送markdown消息
        send_md_msg_text(senderid, text, webhook_url)

    if text_info == "测试":
        p = Popen([sys.executable, "robot220414.py"], stdout=PIPE, stdin=PIPE, stderr=STDOUT)

    if text_info == "说明":
        p = Popen([sys.executable, "钉钉机器人说明.py"], stdout=PIPE, stdin=PIPE, stderr=STDOUT)

    # 统计人数

    if text_info == "统计":
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

        # 调用函数，发送markdown消息
        send_md_msg_text(senderid, text, webhook_url)

    # 取消
    if text_info == "取消":
        if now_time < start_time or end_time < now_time < end_time2:

            file_handle = open(txtname + '.txt', mode='r')
            contentss = str(file_handle.read())
            file_handle.close()
            senderNick = senderNick + '，'
            contentss = str(contentss.replace(senderNick, ''))
            file_handle = open(txtname + '.txt', mode='w')
            file_handle.write(contentss)
            text = '常规餐取消成功'

            file_handle.close()
        else:
            text = '非订餐时间不可取消'
        send_md_msg_text(senderid, text, webhook_url)
    if text_info == "取消轻食":
        file_handle = open(txtname2 + '.txt', mode='r')
        contentss = str(file_handle.read())
        file_handle.close()
        senderNick = senderNick + '，'
        contentss = str(contentss.replace(senderNick, ''))
        file_handle = open(txtname2 + '.txt', mode='w')
        file_handle.write(contentss)
        text = '轻食取消成功'
        send_md_msg_text(senderid, text, webhook_url)

        file_handle.close()

    # 订阅轻食
    if text_info == "订阅轻食":
        senderNick = senderNick + '，'

        file_handle = open('./peoplemessage/订阅轻食.txt', mode='a+')
        file_handle.write(senderNick)
        text = '订阅成功，明日起小G自动帮您预定轻食餐'
        send_md_msg_text(senderid, text, webhook_url)

        file_handle.close()
    if text_info == "取订轻食":
        file_handle = open('./peoplemessage/订阅轻食.txt', mode='r')
        contentss = str(file_handle.read())
        file_handle.close()
        senderNick = senderNick + '，'
        contentss = str(contentss.replace(senderNick, ''))
        file_handle = open('./peoplemessage/订阅轻食.txt', mode='w')
        file_handle.write(contentss)
        text = '取消成功'
        send_md_msg_text(senderid, text, webhook_url)

        file_handle.close()
    if text_info == "取订晚餐":
        file_handle = open('./peoplemessage/订阅晚餐.txt', mode='r')
        contentss = str(file_handle.read())
        file_handle.close()
        senderNick = senderNick + '，'
        contentss = str(contentss.replace(senderNick, ''))
        file_handle = open('./peoplemessage/订阅晚餐.txt', mode='w')
        file_handle.write(contentss)
        text = '取消成功'
        send_md_msg_text(senderid, text, webhook_url)

        file_handle.close()
    if text_info == "取订午餐":
        file_handle = open('./peoplemessage/订阅午餐.txt', mode='r')
        contentss = str(file_handle.read())
        file_handle.close()
        senderNick = senderNick + '，'
        contentss = str(contentss.replace(senderNick, ''))
        file_handle = open('./peoplemessage/订阅午餐.txt', mode='w')
        file_handle.write(contentss)
        text = '取消成功'
        send_md_msg_text(senderid, text, webhook_url)

        file_handle.close()
    if text_info == "订阅晚餐":
        senderNick = senderNick + '，'

        file_handle = open('./peoplemessage/订阅晚餐.txt', mode='a+')
        file_handle.write(senderNick)
        text = '订阅成功，明日起小G自动帮您点晚餐'
        send_md_msg_text(senderid, text, webhook_url)

        file_handle.close()
    if text_info == "订阅午餐":
        senderNick = senderNick + '，'

        file_handle = open('./peoplemessage/订阅午餐.txt', mode='a+')
        file_handle.write(senderNick)
        text = '订阅成功，明日起小G自动帮您点午餐'
        send_md_msg_text(senderid, text, webhook_url)
        file_handle.close()


def handle_info_(req_data):
    text_info = req_data['text']['content'].strip()
    webhook_url = req_data['sessionWebhook']
    senderid = req_data['senderStaffId']
    senderNick = req_data['senderNick']
    if text_info == '上班打卡':
        senderid = "'" + senderid + " ',"

        file_handle = open('./peoplemessage/上班打卡.txt', mode='a+')
        file_handle.write(senderid)

        file_handle.close()
        text = senderid + ' 订阅成功,工作日8.29分还未打卡小G会私聊您'

    else:
        text = "小G很忙"
    send_md_msg_text(senderid, text, webhook_url)


@app.route("/", methods=["POST"])
def get_data():
    # 第一步验证：是否是post请求
    if request.method == "POST":
        # print(request.headers)
        # 签名验证 获取headers中的Timestamp和Sign
        timestamp = request.headers.get('Timestamp')
        sign = request.headers.get('Sign')
        # 第二步验证：签名是否有效
        if check_sig(timestamp) == sign:
            # 获取、处理数据 
            req_data = json.loads(str(request.data, 'utf-8'))
            conversationType = req_data['conversationType']
            if conversationType == '2':
                # print(req_data)
                handle_info(req_data)
                print('群聊验证通过')
                return 'hhh'
            else:
                handle_info_(req_data)
                print('私聊验证通过')
                txtname = './log/' + str(datetime.datetime.now().date().year) + str(
                    datetime.datetime.now().date().month) + str(datetime.datetime.now().date().day)
                now_time = str(datetime.datetime.now())
                file_handle = open(txtname + '.txt', mode='a')
                file_handle.close()

                contentss = str(req_data)

                file_handle = open(txtname + '.txt', mode='a+')

                file_handle.write('\n' + now_time + contentss)
                file_handle.close()

                return 'hhh'

        print('验证不通过')
        return 'ppp'

    print('有get请求')
    return 'sss'


def job():
    print("start job")
    print("hello")


# schedule.every().day.at("15:11").do(job)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8087)
##    schedule.every(10).seconds.do(job)
##    while True:
##        schedule.run_pending()
##        time.sleep(2)
