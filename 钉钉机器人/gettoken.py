import configparser
import json
import requests
import time
import datetime


def configp():
    config = configparser.ConfigParser()
    filename = 'mypy.ini'
    config.read(filename, encoding='utf-8')
    # config.read(open('mypy.ini'))
    appkey = config.get('H5', 'AppKey')
    appsecret = config.get("H5", "AppSecret")
    usermobile = config.get("H5", "usermobile")
    tokentime = config.get("H5", "tokentime")
    acesstoken = config.get("H5", "acesstoken")
    op_user_id = config.get("H5", "op_user_id")
    user_id = config.get("H5", "user_id")
    noon = config.get("H5", "noon")
    evening = config.get("H5", "evening")
    classuser = config.get("H5", "classuser")
    # config.set("H5","acesstoken", "111")
    # config.write(open(filename, 'w'))
    return appkey, appsecret, usermobile, tokentime, acesstoken, user_id, op_user_id, noon, evening, classuser


# 获取h5应用的acess_token,权限比机器人高一些。
def gettoken():
    import time
    con = configp()
    appkey = con[0]
    appsecret = con[1]
    tokentime = con[3]
    acesstoken = con[4]

    nowtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    nowtime = time.strptime(nowtime, "%Y-%m-%d %H:%M:%S")
    tokentime = time.strptime(tokentime, "%Y-%m-%d %H:%M:%S")
    if nowtime >= tokentime:
        url = "https://oapi.dingtalk.com/gettoken?appkey=" + appkey + "&appsecret=" + appsecret
        r = requests.get(url)
        msg = r.json()['errmsg']
        if msg == "ok":
            content = r.json()['access_token']
            s = r.json()['expires_in'] - 200
            time = (datetime.datetime.now() + datetime.timedelta(seconds=s)).strftime("%Y-%m-%d %H:%M:%S")
            config = configparser.ConfigParser()
            filename = 'mypy.ini'
            config.read(filename, encoding='utf-8')
            config.set("H5", "acesstoken", content)
            config.set("H5", "tokentime", time)
            config.write(open(filename, 'w'))
            return msg, content, time
        else:
            return msg
    else:
        return appkey, acesstoken, tokentime


# 获取userid
def getuserid():
    b = gettoken()[1]
    url = "https://oapi.dingtalk.com/topapi/v2/user/getbymobile?access_token="+b+"&mobile=18900739796"
    r = requests.get(url)
    print(r.json())


#  https://oapi.dingtalk.com/topapi/attendance/getsimplegroups?access_token=


# 考勤
# get考勤
# https://oapi.dingtalk.com/topapi/attendance/schedule/listbyday?access_token=cd97bba&op_user_id=190610551937619553&user_id=15954682306537057&date_time=1650355849143
def getrest():
    a = configp()
    b = gettoken()[1]
    now = str(round(time.time() * 1000))
    url = "https://oapi.dingtalk.com/topapi/attendance/schedule/listbyday?access_token=" + b + "&op_user_id=190610551937619553&user_id=15954682306537057&date_time=" + now
    r = requests.get(url)
    is_rest = r.json()['result'][0]['is_rest']
    return is_rest


def getdept():
    b = gettoken()[1]
    url = "https://oapi.dingtalk.com/topapi/v2/department/listsub?access_token=" + b
    r = requests.get(url)
    deptname = r.json()['result'][100]['name']
    return deptname


def getclasscard():
    b = gettoken()[1]
   

    url="https://oapi.dingtalk.com/attendance/listRecord?access_token=" + b
    form={
    "checkDateFrom": "2022-05-07 00:00:00",
    "userIds": [
        "15954682306537057",
        "0519655328698825"
    ],
    "isI18n": "false",
    "checkDateTo": "2022-05-08 00:00:00"
}
    data=json.dumps(form)
    #print (data)
    r = requests.post(url,data)
    if 'timeResult' in r.text:
        return r.text
    else :
        return '1'
    

if __name__ == '__main__':
    aaa = getuserid()
    print(aaa)
