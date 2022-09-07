# Author: sunzy
import random, math, base64
import time

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import requests, re, json, csv
from lxml import etree
from config import password, user_id, course_KCDM, sleep_time

proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}

def encryptPassword(password, key):
    # password 加密, 该段代码参考于 https://github.com/EdenLin-c/CPdaily/blob/master/Jin.py
    def randomString(len):
        retStr = ''
        i = 0
        while i < len:
            retStr += aes_chars[(math.floor(random.random() * aes_chars_len))]
            i = i + 1
        return retStr

    def getAesString(data, key, iv):
        key = re.sub('/(^\s+)|(\s+$)/g', '', key)
        aes = AES.new(str.encode(key), AES.MODE_CBC, str.encode(iv))
        pad_pkcs7 = pad(data.encode('utf-8'), AES.block_size, style='pkcs7')
        encrypted = aes.encrypt(pad_pkcs7)
        return str(base64.b64encode(encrypted), 'utf-8')

    aes_chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678'
    aes_chars_len = len(aes_chars)
    encrypted = getAesString(randomString(64) + password, key, randomString(16))
    return encrypted


def printCourseInfo(course):
    print("[+] 课程名称:", course["BJMC"])
    print("[+] 上课时间和地点:", course["PKSJDDMS"])
    print("[+] 任课教师:", course["RKJS"])

def getSession():
    """
    :return: 返回获取的session
    """
    session_client = requests.Session()
    requests.packages.urllib3.disable_warnings()
    response = session_client.get("https://ids.xidian.edu.cn/authserver/login")

    parse_html = etree.HTML(response.text)
    pwdEncryptSalt = parse_html.xpath('//div//input[@id="pwdEncryptSalt"]//@value')[0]
    execution = parse_html.xpath('//div//input[@id="execution"]//@value')[0]
    encrypt_passwrod = encryptPassword(password, pwdEncryptSalt)

    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Length': '154',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'ids.xidian.edu.cn',
    'Origin': 'http://ids.xidian.edu.cn',
    'Referer': 'http://ids.xidian.edu.cn/authserver/login',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    }

    post_data = {
    "username": user_id,
    "password": encrypt_passwrod,
    "captcha": None,
    "_eventId": "submit",
    "cllt": "userNameLogin",
    "dllt": "generalLogin",
    "lt": None,
    "execution": execution
    }
    sso_response = session_client.post("https://ids.xidian.edu.cn/authserver/login", headers=headers, data=post_data,verify=False)
    return session_client

def getCourseInfo(session_client, course_KCDM):
    """
    获取指定课程的详细信息
    :param session_client:
    :param course_KCDM:
    :return:
    """
    # course_KCDM = ""
    course_infos = session_client.post("https://yjspt.xidian.edu.cn/yjsxkapp/sys/xsxkapp/xsxkCourse/loadJhnCourseInfo.do?query_keyword=" + course_KCDM,  verify = False)
    course_json = json.loads(course_infos.text)["datas"]
    if len(course_json) == 0:

        return None
    course_info = ""
    for course in course_json:
        if course_KCDM == course["KCDM"]:
            course_info = course
            break
    return course_info

def chooseCourse(course_BJDM):
    """
    选课函数，根据course_BJDM进行选课
    :param course_BJDM:
    :return:
    """
    csrf_token_url = "https://yjspt.xidian.edu.cn/yjsxkapp/sys/xsxkapp/xsxkHome/loadPublicInfo_course.do"
    csrf_response = session_client.get(csrf_token_url).text
    json_csrf_res = json.loads(csrf_response)
    csrf_token = json_csrf_res.get("csrfToken")
    choose_course_url = "https://yjspt.xidian.edu.cn/yjsxkapp/sys/xsxkapp/xsxkCourse/choiceCourse.do?bjdm={0}&csrfToken={1}&lx=0".format(course_BJDM, csrf_token)
    choose_response = session_client.get(choose_course_url, verify = False).text
    # print(choose_response)
    return json.loads(choose_response)["code"]

if __name__ == '__main__':
    KCDM = course_KCDM
    session_client = getSession()
    course_info = getCourseInfo(session_client = session_client, course_KCDM = KCDM)
    if course_info == None:
        print("[+] 未查询到课程信息，请检查课程代码！")
        quit()
    course_KXRS = course_info["KXRS"]  # 课程总容量
    course_DQRS = course_info["DQRS"]  # 当前选课人数

    while True:
        if course_DQRS < course_KXRS:
            course_BJDM = course_info["BJDM"]
            code = chooseCourse(course_BJDM)
            if code == 1:
                print("[+] 选课成功!")
                print("[+] 课程信息如下:")
                printCourseInfo(course_info)
                quit()
            else:
                print("[+] 选课失败!")
        else:
            print("[+] 当前课程容量已满!")
            time.sleep(sleep_time)    # 每60s查询一次
            continue
        # 监控选课人数的变化
        course_info = getCourseInfo(session_client=session_client, course_KCDM = KCDM)
        course_KXRS = course_info["KXRS"]  # 课程总容量
        course_DQRS = course_info["DQRS"]  # 当前选课人数
    print("[+] Finish")
