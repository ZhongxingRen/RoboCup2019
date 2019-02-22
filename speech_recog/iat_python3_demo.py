# -*- coding: utf-8 -*-
import requests
import time
import hashlib
import base64

URL = "http://api.xfyun.cn/v1/service/v1/iat"
APPID = "5c487dc0"
API_KEY = "588f3f2f7a18769bafc778fdca809a9b"


def getHeader(aue, engineType):
    curTime = str(int(time.time()))
    # curTime = '1526542623'
    param = "{\"aue\":\"" + aue + "\"" + ",\"engine_type\":\"" + engineType + "\"}"
    print("param:{}".format(param))
    paramBase64 = str(base64.b64encode(param.encode('utf-8')), 'utf-8')
    print("x_param:{}".format(paramBase64))

    m2 = hashlib.md5()
    m2.update((API_KEY + curTime + paramBase64).encode('utf-8'))
    checkSum = m2.hexdigest()
    print('checkSum:{}'.format(checkSum))
    header = {
        'X-CurTime': curTime,
        'X-Param': paramBase64,
        'X-Appid': APPID,
        'X-CheckSum': checkSum,
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }
    print(header)
    return header


def getBody(filepath):
    binfile = open(filepath, 'rb')
    data = {'audio': base64.b64encode(binfile.read())}
    print(data)
    print('data:{}'.format(type(data['audio'])))
    # print("type(data['audio']):{}".format(type(data['audio'])))
    return data


aue = "raw"
engineType = "sms-en16k"
audioFilePath = "/home/jiashi/src/robocup_pepper/catkin_ws/src/Kamerider_pepper/pepper.mp3"

r = requests.post(URL, headers=getHeader(aue, engineType), data=getBody(audioFilePath))
print(r.content.decode('utf-8'))
