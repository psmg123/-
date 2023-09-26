import time
from threading import Thread
import requests
import base64
from PIL import Image
from io import BytesIO
import ddddocr
import execjs

import schedule

ocr = ddddocr.DdddOcr()


class student():
    def __init__(self, name, password, classid=3):
        self.name = name
        self.password = password
        self.mingzhi = ""
        self.classid = classid
        self.classname = ""
        self.cookie = ""
        self.LoginOne()

    def getUuidandToken(self):
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Authorization': '',
            'Cache-Control': 'no-cache',
            # 'Content-Length': '0',
            # Requests sorts cookies= alphabetically
            # 'Cookie': 'zg_did=%7B%22did%22%3A%20%2218718dd3bfe2c5-0057101a4577dd-7a545470-144000-18718dd3bff1149%22%7D; zg_=%7B%22sid%22%3A%201679893457021%2C%22updated%22%3A%201679893457023%2C%22info%22%3A%201679749364738%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22ehall.wspc.edu.cn%22%2C%22cuid%22%3A%20%22202107010115%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%2C%22firstScreen%22%3A%201679893457021%7D; Authorization=eyJhbGciOiJIUzUxMiJ9.eyJ0aW1lIjoxNjk0MDA0ODU1MTQ2LCJsb2dpbl91c2VyX2tleSI6IjIwMjEwNzAxMDExNSIsInRva2VuIjoiN2ZtbWtxOTZyMmlsanI3ZXZvdXFkODA1aGgifQ.iUNqwA2wFGN5zswUbDn22NcyJlpCLhciK3zrooM6IagifuCHqP_hQz3yq73J6q-C2EoXHxpKbvA7FNKqEZGEUA',
            'Origin': 'http://jwxk.wspc.edu.cn',
            'Pragma': 'no-cache',
            'Proxy-Connection': 'keep-alive',
            'Referer': 'http://jwxk.wspc.edu.cn/xsxk/profile/index.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69',
        }

        response = requests.post('http://jwxk.wspc.edu.cn/xsxk/auth/captcha', headers=headers, verify=False)
        imgbase64 = response.json()['data']['captcha'].lstrip("data:image/png;base64")
        uuid = response.json()['data']['uuid']
        # print(uuid)
        # print(imgbase64)
        # Base64编码的图像数据

        # 解码Base64数据
        image_data = base64.b64decode(imgbase64)

        # 创建一个BytesIO对象以读取图像数据
        image_stream = BytesIO(image_data)

        # 打开图像并保存为文件（这里假设是PNG格式）
        image = Image.open(image_stream)
        image.save("output.png", "PNG")

        # # 可以选择显示图像
        # image.show()
        res = ocr.classification(image)
        # print('识别出的验证码为：' + res)

        return {"uuid": uuid, "captcha": res}

    def login(self, loginname, password, captcha, uuid):
        cookies = {
            'zg_did': '%7B%22did%22%3A%20%2218718dd3bfe2c5-0057101a4577dd-7a545470-144000-18718dd3bff1149%22%7D',
            'zg_': '%7B%22sid%22%3A%201679893457021%2C%22updated%22%3A%201679893457023%2C%22info%22%3A%201679749364738%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22ehall.wspc.edu.cn%22%2C%22cuid%22%3A%20%22202107010115%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%2C%22firstScreen%22%3A%201679893457021%7D',
            'Authorization': 'eyJhbGciOiJIUzUxMiJ9.eyJ0aW1lIjoxNjk0MDA0ODU1MTQ2LCJsb2dpbl91c2VyX2tleSI6IjIwMjEwNzAxMDExNSIsInRva2VuIjoiN2ZtbWtxOTZyMmlsanI3ZXZvdXFkODA1aGgifQ.iUNqwA2wFGN5zswUbDn22NcyJlpCLhciK3zrooM6IagifuCHqP_hQz3yq73J6q-C2EoXHxpKbvA7FNKqEZGEUA',
        }

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Authorization': '',
            'Cache-Control': 'no-cache',
            # Requests sorts cookies= alphabetically
            # 'Cookie': 'zg_did=%7B%22did%22%3A%20%2218718dd3bfe2c5-0057101a4577dd-7a545470-144000-18718dd3bff1149%22%7D; zg_=%7B%22sid%22%3A%201679893457021%2C%22updated%22%3A%201679893457023%2C%22info%22%3A%201679749364738%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22ehall.wspc.edu.cn%22%2C%22cuid%22%3A%20%22202107010115%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%2C%22firstScreen%22%3A%201679893457021%7D; Authorization=eyJhbGciOiJIUzUxMiJ9.eyJ0aW1lIjoxNjk0MDA0ODU1MTQ2LCJsb2dpbl91c2VyX2tleSI6IjIwMjEwNzAxMDExNSIsInRva2VuIjoiN2ZtbWtxOTZyMmlsanI3ZXZvdXFkODA1aGgifQ.iUNqwA2wFGN5zswUbDn22NcyJlpCLhciK3zrooM6IagifuCHqP_hQz3yq73J6q-C2EoXHxpKbvA7FNKqEZGEUA',
            'Origin': 'http://jwxk.wspc.edu.cn',
            'Pragma': 'no-cache',
            'Proxy-Connection': 'keep-alive',
            'Referer': 'http://jwxk.wspc.edu.cn/xsxk/profile/index.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69',
        }

        data = {
            'loginname': loginname,
            'password': password,
            'captcha': captcha,
            'uuid': uuid,
        }

        response = requests.post('http://jwxk.wspc.edu.cn/xsxk/auth/login', cookies=cookies, headers=headers, data=data,
                                 verify=False)
        # print(response.json()['data']['token'],"111111")
        try:
            self.mingzhi = response.json()['data']['student']['XM']
            return response.json()['data']['token']
        except:
            return -1

    def getClass(self, Authorization: str, secretVal: str, clazzId: str):
        cookies = {
            # 'zg_did': '%7B%22did%22%3A%20%2218718dd3bfe2c5-0057101a4577dd-7a545470-144000-18718dd3bff1149%22%7D',
            # 'zg_': '%7B%22sid%22%3A%201679893457021%2C%22updated%22%3A%201679893457023%2C%22info%22%3A%201679749364738%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22ehall.wspc.edu.cn%22%2C%22cuid%22%3A%20%22202107010115%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%2C%22firstScreen%22%3A%201679893457021%7D',
            # 'Authorization': Authorization,

        }

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Authorization': Authorization,
            'Cache-Control': 'no-cache',
            # Requests sorts cookies= alphabetically
            # 'Cookie': 'zg_did=%7B%22did%22%3A%20%2218718dd3bfe2c5-0057101a4577dd-7a545470-144000-18718dd3bff1149%22%7D; zg_=%7B%22sid%22%3A%201679893457021%2C%22updated%22%3A%201679893457023%2C%22info%22%3A%201679749364738%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22ehall.wspc.edu.cn%22%2C%22cuid%22%3A%20%22202107010115%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%2C%22firstScreen%22%3A%201679893457021%7D; Authorization=eyJhbGciOiJIUzUxMiJ9.eyJ0aW1lIjoxNjk0MDEwMTk5MTk4LCJsb2dpbl91c2VyX2tleSI6IjIwMjEwNzAxMDExNSIsInRva2VuIjoiMmpkZjZzOHJwZWp1Z3ByYjYxYTgyM29mZDYifQ.1sIN_kNm8wa-kIdrt3Xs7dwz70bp2NNSQUJjC7whxcW-62qtJNkXEtY2yVZQ6kheuhIanrTCTwHA3NhWmEWIHQ',
            'Origin': 'http://jwxk.wspc.edu.cn',
            'Pragma': 'no-cache',
            'Proxy-Connection': 'keep-alive',
            'Referer': 'http://jwxk.wspc.edu.cn/xsxk/elective/grablessons?batchId=76322f389d1341fab18db8e0a5db64b8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69',
            'batchId': '76322f389d1341fab18db8e0a5db64b8',
        }

        data = {
            'clazzType': 'XGKC',
            'clazzId': clazzId,
            'secretVal': secretVal,
        }

        response = requests.post('http://jwxk.wspc.edu.cn/xsxk/elective/clazz/add', cookies=cookies, headers=headers,
                                 data=data, verify=False)
        print(response.json())

    def getSecretVal(self, Authorization,cid):
        cookies = {
            # 'zg_did': '%7B%22did%22%3A%20%2218718dd3bfe2c5-0057101a4577dd-7a545470-144000-18718dd3bff1149%22%7D',
            # 'zg_': '%7B%22sid%22%3A%201679893457021%2C%22updated%22%3A%201679893457023%2C%22info%22%3A%201679749364738%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22ehall.wspc.edu.cn%22%2C%22cuid%22%3A%20%22202107010115%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%2C%22firstScreen%22%3A%201679893457021%7D',
            # 'Authorization': 'eyJhbGciOiJIUzUxMiJ9.eyJ0aW1lIjoxNjk0MDEwODIxNjgzLCJsb2dpbl91c2VyX2tleSI6IjIwMjEwNzAxMDExNSIsInRva2VuIjoicXZwNTgzdmJwZWp1Y29wNW40OGljN2pra2QifQ.uT2zxBCZ8KbYUfCowy1Ox0Nq4X46rlCNwydYkoKb2N9BiEn5F1htfPN1u7smSaapMA_BhSGJJsEMO41aU50ixg',

        }

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Authorization': Authorization,
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json;charset=UTF-8',
            # Requests sorts cookies= alphabetically
            # 'Cookie': 'zg_did=%7B%22did%22%3A%20%2218718dd3bfe2c5-0057101a4577dd-7a545470-144000-18718dd3bff1149%22%7D; zg_=%7B%22sid%22%3A%201679893457021%2C%22updated%22%3A%201679893457023%2C%22info%22%3A%201679749364738%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22ehall.wspc.edu.cn%22%2C%22cuid%22%3A%20%22202107010115%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%2C%22firstScreen%22%3A%201679893457021%7D; Authorization=eyJhbGciOiJIUzUxMiJ9.eyJ0aW1lIjoxNjk0MDEwODIxNjgzLCJsb2dpbl91c2VyX2tleSI6IjIwMjEwNzAxMDExNSIsInRva2VuIjoicXZwNTgzdmJwZWp1Y29wNW40OGljN2pra2QifQ.uT2zxBCZ8KbYUfCowy1Ox0Nq4X46rlCNwydYkoKb2N9BiEn5F1htfPN1u7smSaapMA_BhSGJJsEMO41aU50ixg',
            'Origin': 'http://jwxk.wspc.edu.cn',
            'Pragma': 'no-cache',
            'Proxy-Connection': 'keep-alive',
            'Referer': 'http://jwxk.wspc.edu.cn/xsxk/elective/grablessons?batchId=76322f389d1341fab18db8e0a5db64b8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69',
            'batchId': '76322f389d1341fab18db8e0a5db64b8',
        }

        json_data = {
            'teachingClassType': 'XGKC',
            'pageNumber': 1,
            'pageSize': 10,
            'orderBy': '',
            'campus': '01',
        }

        response = requests.post('http://jwxk.wspc.edu.cn/xsxk/elective/clazz/list', cookies=cookies, headers=headers,
                                 json=json_data, verify=False)

        # print(type(cid))
        # print(type(0))

        self.classname = response.json()['data']['rows'][cid]['KCM']
        # print(response.json()['data']['rows'][cid]['KCM'])
        # print(response.json()['data']['rows'][cid]['secretVal'])
        # print(response.json()['data']['rows'][cid]['secretVal'])
        return {'secretVal': response.json()['data']['rows'][cid]['secretVal'],
                "clazzId": response.json()['data']['rows'][cid]['JXBID']}


    def LoginOne(self):

        # print(loginname, password, captcha, uuid)
        cookie = None
        while (1):
            dict = self.getUuidandToken()
            # print([dict['captcha'],
            #        dict['uuid']])
            js = open("getpassword.js", mode='r').read()
            ctx = execjs.compile(js)
            # print(ctx.call("aesUtil.encrypt", 302517, "MWMqg2tPcDkxcm11"))
            loginname = self.name
            p = self.password
            password = ctx.call("aesUtil.encrypt", p, "MWMqg2tPcDkxcm11")
            captcha = dict['captcha']
            uuid = dict['uuid']
            res = self.login(loginname, password, captcha, uuid)
            if (res == -1):
                print("失败重新登录")
            else:
                cookie = self.login(loginname, password, captcha, uuid)
                break

        self.cookie = cookie

    def start(self):
        cookie1 = self.cookie
        # print(cookie1)
        for i in range(9):
            # time.sleep(0.5)
            self.classid=i
            print(self.mingzhi, "开始抢课 课程名为: ", self.classname, " id 为:", self.classid)

            secretVal = self.getSecretVal(cookie1,i)
            # print(secretVal)
            self.getClass(cookie1, secretVal['secretVal'], secretVal['clazzId'])



huangyuanzhang = student("202107010108", "061456")
caowenlong = student("202107010131", "137513")
duanshen = student("202107020430", "150818")





def mainq():
    while(1):
        while(1):
            try:
                time.sleep(0.5)
                wangjunjie.start()
                huangyuanzhang.start()
                caowenlong.start()
                duanshen.start()
            except:
                wangjunjie = student("202107010115", "302517")
                huangyuanzhang = student("202107010108", "061456")
                caowenlong = student("202107010131", "137513")
                duanshen = student("202107020430", "150818")


mainq()

# schedule.every().day.at("00:05").do(mainq)


# schedule.every().day.at("06:59:59").do(mainq)
# while True:
#     schedule.run_pending()
