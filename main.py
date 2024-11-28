import time
import random
import json
import base64
import rsa
import requests
import re
import os


# 企业微信webhook推送信息 启用1 禁用0
qywx_push = 1
msg_c = "☁️天翼云盘签到☁️"


BI_RM = list("0123456789abcdefghijklmnopqrstuvwxyz")
B64MAP = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

usernames = os.getenv('USERNAME')
passwords = os.getenv('PASSWORD')
usernames = usernames.replace('，', ',').strip()
passwords = passwords.replace('，', ',').strip()
ty_usernames = usernames.split(',')
ty_passwords = passwords.split(',')

# 将用户名和密码组合成一个列表
accounts = [{"username": u, "password": p} for u, p in zip(ty_usernames, ty_passwords)]

def int2char(a):
    return BI_RM[a]

def b64tohex(a):
    d = ""
    e = 0
    c = 0
    for i in range(len(a)):
        if a[i] != "=":
            v = B64MAP.index(a[i])
            if e == 0:
                e = 1
                d += int2char(v >> 2)
                c = 3 & v
            elif e == 1:
                e = 2
                d += int2char(c << 2 | v >> 4)
                c = 15 & v
            elif e == 2:
                e = 3
                d += int2char(c)
                d += int2char(v >> 2)
                c = 3 & v
            else:
                e = 0
                d += int2char(c << 2 | v >> 4)
                d += int2char(15 & v)
    if e == 1:
        d += int2char(c << 2)
    return d

def rsa_encode(j_rsakey, string):
    rsa_key = f"-----BEGIN PUBLIC KEY-----\n{j_rsakey}\n-----END PUBLIC KEY-----"
    pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(rsa_key.encode())
    result = b64tohex((base64.b64encode(rsa.encrypt(f'{string}'.encode(), pubkey))).decode())
    return result

def login(username, password):
    global msg_c
    urlToken = "https://m.cloud.189.cn/udb/udb_login.jsp?pageId=1&pageKey=default&clientType=wap&redirectURL=https://m.cloud.189.cn/zhuanti/2021/shakeLottery/index.html"
    s = requests.Session()
    r = s.get(urlToken)
    pattern = r"https?://[^\s'\"]+"  # 匹配以http或https开头的url
    match = re.search(pattern, r.text)  # 在文本中搜索匹配
    if match:  # 如果找到匹配
        url = match.group()  # 获取匹配的字符串
    else:  # 如果没有找到匹配
        print("没有找到url")
        return None

    r = s.get(url)
    pattern = r"<a id=\"j-tab-login-link\"[^>]*href=\"([^\"]+)\""  # 匹配id为j-tab-login-link的a标签，并捕获href引号内的内容
    match = re.search(pattern, r.text)  # 在文本中搜索匹配
    if match:  # 如果找到匹配
        href = match.group(1)  # 获取捕获的内容
    else:  # 如果没有找到匹配
        print("没有找到href链接")
        return None

    r = s.get(href)
    captchaToken = re.findall(r"captchaToken' value='(.+?)'", r.text)[0]
    lt = re.findall(r'lt = "(.+?)"', r.text)[0]
    returnUrl = re.findall(r"returnUrl= '(.+?)'", r.text)[0]
    paramId = re.findall(r'paramId = "(.+?)"', r.text)[0]
    j_rsakey = re.findall(r'j_rsaKey" value="(\S+)"', r.text, re.M)[0]
    s.headers.update({"lt": lt})

    username = rsa_encode(j_rsakey, username)
    password = rsa_encode(j_rsakey, password)
    url = "https://open.e.189.cn/api/logbox/oauth2/loginSubmit.do"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/76.0',
        'Referer': 'https://open.e.189.cn/',
    }
    data = {
        "appKey": "cloud",
        "accountType": '01',
        "userName": f"{{RSA}}{username}",
        "password": f"{{RSA}}{password}",
        "validateCode": "",
        "captchaToken": captchaToken,
        "returnUrl": returnUrl,
        "mailSuffix": "@189.cn",
        "paramId": paramId
    }
    r = s.post(url, data=data, headers=headers, timeout=5)
    if r.json().get('result', None) == 0:
        print(f"🥳{r.json()['msg']}🥳")
        msg_c += f"\n🥳{r.json()['msg']}🥳"
    else:
        print(f"😭{r.json()['msg']}😭")
        msg_c += f"\n🥳{r.json()['msg']}🥳"
    redirect_url = r.json()['toUrl']
    r = s.get(redirect_url)
    return s

def main():
    global msg_c
    num = 1
    for account in accounts:
        username = account["username"]
        password = account["password"]
        session = login(username, password)
        if session is not None:
            rand = str(round(time.time() * 1000))
            surl = f'https://api.cloud.189.cn/mkt/userSign.action?rand={rand}&clientType=TELEANDROID&version=8.6.3&model=Pixel 2'
            url = f'https://m.cloud.189.cn/v2/drawPrizeMarketDetails.action?taskId=TASK_SIGNIN&activityId=ACT_SIGNIN'
            url2 = f'https://m.cloud.189.cn/v2/drawPrizeMarketDetails.action?taskId=TASK_SIGNIN_PHOTOS&activityId=ACT_SIGNIN'
            url3 = f'https://m.cloud.189.cn/v2/drawPrizeMarketDetails.action?taskId=TASK_2022_FLDFS_KJ&activityId=ACT_SIGNIN'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.118 Mobile Safari/537.36 Ecloud/8.6.3 Android/26 clientId/355325117317828 clientModel/Pixel 2 imsi/460071114317824 clientChannelId/qq proVersion/1.0.6',
                "Referer": "https://m.cloud.189.cn/zhuanti/2016/sign/index.jsp?albumBackupOpened=1",
                "Host": "m.cloud.189.cn",
                "Accept-Encoding": "gzip, deflate",
            }
            response = session.get(surl, headers=headers)
            netdiskBonus = response.json()['netdiskBonus']
            if response.json()['isSign'] == "false":
                print(f"🆔账号{num} 🎁签到获得{netdiskBonus}M空间🎉🎉")
                msg_c += f"\n🆔账号{num} 🎁签到获得{netdiskBonus}M空间🎉🎉"
            else:
                print(f"🆔账号{num} 已经签到过了")
                msg_c += f"\n🆔账号{num} 已经签到过了"

            response = session.get(url, headers=headers)
            if "errorCode" in response.text:
                if "User_Not_Chance" in response.text:
                    print(f"🆔账号{num} 🥰抽奖1：已经抽奖过了🥰")
                    msg_c += f"\n🆔账号{num} 🥰抽奖1：已经抽奖过了🥰"
                else:
                    print(f"🆔账号{num} {response.text}")
                    msg_c += f"\n🆔账号{num} {response.text}"
            else:
                description = response.json()['description']
                print(f"🆔账号{num} 🎁抽奖1：获得{description}🎉🎉")
                msg_c += f"\n🆔账号{num} 🎁抽奖1：获得{description}🎉🎉"

            time.sleep(random.randint(5, 10))  
            response = session.get(url2, headers=headers)
            if "errorCode" in response.text:
                if "User_Not_Chance" in response.text:
                    print(f"🆔账号{num} 🥰抽奖2：已经抽奖过了🥰")
                    msg_c += f"\n🆔账号{num} 🥰抽奖2：已经抽奖过了🥰"
                else:
                    print(f"🆔账号{num} {response.text}")
                    msg_c += f"\n🆔账号{num} {response.text}"
            else:
                description = response.json()['prizeName']
                print(f"🆔账号{num} 🎁抽奖2：获得{description}🎉🎉")
                msg_c += f"\n🆔账号{num} 🎁抽奖2：获得{description}🎉🎉"

            time.sleep(random.randint(5, 10))      
            response = session.get(url3, headers=headers)
            if "errorCode" in response.text:
                if "User_Not_Chance" in response.text:
                    print(f"🆔账号{num} 🥰抽奖3：已经抽奖过了🥰")
                    msg_c += f"\n🆔账号{num} 🥰抽奖3：已经抽奖过了🥰"
                else:
                    print(f"🆔账号{num} 抽奖3：{response.text}")
                    msg_c += f"\n🆔账号{num} 抽奖3：{response.text}"
            else:
                description = response.json()['prizeName']
                print(f"🆔账号{num} 🎁抽奖3：获得{description}🎉🎉")
                msg_c += f"\n🆔账号{num} 🎁抽奖3：获得{description}🎉🎉"
            num += 1

def send_msg():
    
    if qywx_push == 1:

        webhook_url = os.getenv('WEBHOOK')
        if webhook_url is not None:
            data = {
                "msgtype": "text",
                "text": {
                    "content": msg_c
                }
            }
            response = requests.post(webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
            if response.status_code == 200:
                print("发送成功")
                print(response.json())
            else:
                print(f"请求失败，状态码: {response.status_code}")
                print(response.text)

        else:
            print("环境变量 WEBHOOK 不存在\n请在github - settings - Secrets and variables - Actions - New repository secret\n请以上路径手动添加名称为WEBHOOK，值为企业微信webhook地址的密钥键值")




if __name__ == "__main__":
    main()
    send_msg()
