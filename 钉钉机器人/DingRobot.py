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


# ??????????????????????????????
def check_sig(timestamp):
    app_secret = 'ZN4yoH2gwrjoIb3FCO0LdDu0_'
    app_secret_enc = app_secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, app_secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(app_secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = base64.b64encode(hmac_code).decode('utf-8')
    return sign


# ??????txt??????
def send_md_msg_text(senderid, message, webhook_url):
    data = {"msgtype": "text", "text": {"content": message}, "at": {"atUserIds": [senderid], "isAtAll": False}}
    # ??????requests??????post??????
    req = requests.post(webhook_url, json=data)


# ??????markdown??????
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
    # ??????requests??????post??????
    req = requests.post(webhook_url, json=data)


# ????????????????????????
def handle_info(req_data):
    txtname = timetxt()[0]
    txtname2 = timetxt()[1]
    news = str(getnew())
    # ???????????????????????? ??????webhook_url 
    text_info = req_data['text']['content'].strip()
    webhook_url = req_data['sessionWebhook']
    senderid = req_data['senderStaffId']
    senderNick = req_data['senderNick']
    conversationTitle = req_data['conversationTitle']
    createAt = str(req_data['createAt'])
    # senderStaffId=req_data['senderStaffId']
    # print('***************text_info???', text_info)
    # ??????sendeNIck

    # ?????????????????? 220509
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
                copy = senderNick + ",???????????????????"
            else:
                file_handle.write(senderNick + '???')
                file_handle.close()
                file_handle = open(txtname + '.txt', mode='r+')
            contents = str(file_handle.read())
            file_handle.close()
            if senderNick in contentss:
                title = "??????"
                text = copy + '\n\r' + """\n
    ![screenshot](https://staticedu-wps.cache.iciba.com/image/ea7edf9186d6a66b1439f6380d9ce964.jpg)\n>
    **[????????????](https://www.baidu.com/)**\n>
                    """ + news + "\n"

            # ?????????????????????markdown??????
            # send_md_msg( senderid,title,text, webhook_url)
        else:
            text = "???????????????????????????,??????10:50??????,??????16:30??????"
            send_md_msg_text(senderid, text, webhook_url)

    if text_info == "2":
        if now_time <= end_time2:
            file_handle = open(txtname2 + '.txt', mode='a')
            file_handle.close()
            file_handle = open(txtname2 + '.txt', mode='r+')
            contentss = str(file_handle.read())
            if senderNick not in contentss:
                file_handle.write(senderNick + '???')
            file_handle.close()
        else:
            text = "???????????????????????????,??????10:50??????,??????16:30??????"
            send_md_msg_text(senderid, text, webhook_url)

    if text_info == "11":
        file_handle = open(txtname + '.txt', mode='a+')
        file_handle.write(senderNick + '???')

        file_handle.close()

        text = senderNick + "??????????????????" + "\n" + createAt
        # ?????????????????????markdown??????
        send_md_msg_text(senderid, text, webhook_url)

    if text_info == "??????":
        p = Popen([sys.executable, "robot220414.py"], stdout=PIPE, stdin=PIPE, stderr=STDOUT)

    if text_info == "??????":
        p = Popen([sys.executable, "?????????????????????.py"], stdout=PIPE, stdin=PIPE, stderr=STDOUT)

    # ????????????

    if text_info == "??????":
        if pathlib.Path(txtname + '.txt').exists() and pathlib.Path(txtname2 + '.txt').exists():
            file_handle = open(txtname + '.txt').read()
            f = str(file_handle.count('???'))

            file_handle = open(txtname + '.txt', mode='r')
            contents = str(file_handle.read())
            file_handle.close()
            # ??????
            file_handle = open(txtname2 + '.txt').read()
            g = str(file_handle.count('???'))

            file_handle = open(txtname2 + '.txt', mode='r')
            contents2 = str(file_handle.read())
            file_handle.close()
            # ???????????????
            txtname3 = lightmeal.getrest()
            file_handle = open(txtname3 + '.txt').read()
            h = str(file_handle.count('???'))

            file_handle = open(txtname3 + '.txt', mode='r')
            contents3 = str(file_handle.read())
            file_handle.close()
            if now_time < end_time:
                text = '???????????????????????????' + h + '???:' + contents3 + '\n &\n' + '????????????????????????' + f + '???:' + contents + '\n &\n' + '????????????????????????????????????' + g + '???:' + contents2
            else:
                text = '????????????????????????' + f + '???:' + contents + '\n &\n' + '????????????????????????????????????' + g + '???:' + contents2
        elif pathlib.Path(txtname + '.txt').exists() and pathlib.Path(txtname2 + '.txt').exists() == False:
            file_handle = open(txtname + '.txt').read()
            f = str(file_handle.count('???'))

            file_handle = open(txtname + '.txt', mode='r')
            contents = str(file_handle.read())
            file_handle.close()
            text = '????????????????????????' + f + '???:' + contents
        elif pathlib.Path(txtname + '.txt').exists() == False and pathlib.Path(txtname2 + '.txt').exists():
            file_handle = open(txtname2 + '.txt', mode='r')
            g = str(file_handle.count('???'))
            contents2 = str(file_handle.read())
            file_handle.close()
            text = '??????????????????????????????' + g + '???:' + contents2
        else:
            text = '???????????????????????????'

        # ?????????????????????markdown??????
        send_md_msg_text(senderid, text, webhook_url)

    # ??????
    if text_info == "??????":
        if now_time < start_time or end_time < now_time < end_time2:

            file_handle = open(txtname + '.txt', mode='r')
            contentss = str(file_handle.read())
            file_handle.close()
            senderNick = senderNick + '???'
            contentss = str(contentss.replace(senderNick, ''))
            file_handle = open(txtname + '.txt', mode='w')
            file_handle.write(contentss)
            text = '?????????????????????'

            file_handle.close()
        else:
            text = '???????????????????????????'
        send_md_msg_text(senderid, text, webhook_url)
    if text_info == "????????????":
        file_handle = open(txtname2 + '.txt', mode='r')
        contentss = str(file_handle.read())
        file_handle.close()
        senderNick = senderNick + '???'
        contentss = str(contentss.replace(senderNick, ''))
        file_handle = open(txtname2 + '.txt', mode='w')
        file_handle.write(contentss)
        text = '??????????????????'
        send_md_msg_text(senderid, text, webhook_url)

        file_handle.close()

    # ????????????
    if text_info == "????????????":
        senderNick = senderNick + '???'

        file_handle = open('./peoplemessage/????????????.txt', mode='a+')
        file_handle.write(senderNick)
        text = '???????????????????????????G???????????????????????????'
        send_md_msg_text(senderid, text, webhook_url)

        file_handle.close()
    if text_info == "????????????":
        file_handle = open('./peoplemessage/????????????.txt', mode='r')
        contentss = str(file_handle.read())
        file_handle.close()
        senderNick = senderNick + '???'
        contentss = str(contentss.replace(senderNick, ''))
        file_handle = open('./peoplemessage/????????????.txt', mode='w')
        file_handle.write(contentss)
        text = '????????????'
        send_md_msg_text(senderid, text, webhook_url)

        file_handle.close()
    if text_info == "????????????":
        file_handle = open('./peoplemessage/????????????.txt', mode='r')
        contentss = str(file_handle.read())
        file_handle.close()
        senderNick = senderNick + '???'
        contentss = str(contentss.replace(senderNick, ''))
        file_handle = open('./peoplemessage/????????????.txt', mode='w')
        file_handle.write(contentss)
        text = '????????????'
        send_md_msg_text(senderid, text, webhook_url)

        file_handle.close()
    if text_info == "????????????":
        file_handle = open('./peoplemessage/????????????.txt', mode='r')
        contentss = str(file_handle.read())
        file_handle.close()
        senderNick = senderNick + '???'
        contentss = str(contentss.replace(senderNick, ''))
        file_handle = open('./peoplemessage/????????????.txt', mode='w')
        file_handle.write(contentss)
        text = '????????????'
        send_md_msg_text(senderid, text, webhook_url)

        file_handle.close()
    if text_info == "????????????":
        senderNick = senderNick + '???'

        file_handle = open('./peoplemessage/????????????.txt', mode='a+')
        file_handle.write(senderNick)
        text = '???????????????????????????G?????????????????????'
        send_md_msg_text(senderid, text, webhook_url)

        file_handle.close()
    if text_info == "????????????":
        senderNick = senderNick + '???'

        file_handle = open('./peoplemessage/????????????.txt', mode='a+')
        file_handle.write(senderNick)
        text = '???????????????????????????G?????????????????????'
        send_md_msg_text(senderid, text, webhook_url)
        file_handle.close()


def handle_info_(req_data):
    text_info = req_data['text']['content'].strip()
    webhook_url = req_data['sessionWebhook']
    senderid = req_data['senderStaffId']
    senderNick = req_data['senderNick']
    if text_info == '????????????':
        senderid = "'" + senderid + " ',"

        file_handle = open('./peoplemessage/????????????.txt', mode='a+')
        file_handle.write(senderid)

        file_handle.close()
        text = senderid + ' ????????????,?????????8.29??????????????????G????????????'

    else:
        text = "???G??????"
    send_md_msg_text(senderid, text, webhook_url)


@app.route("/", methods=["POST"])
def get_data():
    # ???????????????????????????post??????
    if request.method == "POST":
        # print(request.headers)
        # ???????????? ??????headers??????Timestamp???Sign
        timestamp = request.headers.get('Timestamp')
        sign = request.headers.get('Sign')
        # ????????????????????????????????????
        if check_sig(timestamp) == sign:
            # ????????????????????? 
            req_data = json.loads(str(request.data, 'utf-8'))
            conversationType = req_data['conversationType']
            if conversationType == '2':
                # print(req_data)
                handle_info(req_data)
                print('??????????????????')
                return 'hhh'
            else:
                handle_info_(req_data)
                print('??????????????????')
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

        print('???????????????')
        return 'ppp'

    print('???get??????')
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
