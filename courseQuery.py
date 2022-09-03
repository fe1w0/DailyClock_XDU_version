# Author: fe1w0
import random, math, base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import requests, re, json, csv
from lxml import etree
from config import password, user_id


proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}

def regx_lesson(tmp_course_item):
    pattern = re.compile(r'\[(\d)-(\d+)节\]')
    start_lesson, end_lesson = pattern.findall(tmp_course_item)[0]
    return start_lesson, end_lesson

def regx_classroom(tmp_course_item):
    pattern = re.compile(r'\](.*?)$')
    classroom = pattern.findall(tmp_course_item)[0]
    return classroom

def case_day(course_day):
    days = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    return days.index(course_day) + 1
 
def parse_PKSJDD(tmp_wakeup_course_list):
    # 解析 PKSJDD 参数，并生成 wakeup_course_list
    wakeup_course_list = []
    for course in tmp_wakeup_course_list:
        items = course["PKSJDD"].split(";")
        for item in items:
            course_week = item.split(" ")[0].replace(",", "、").replace("周", "")
            tmp_course_item = item.split(" ")[1]
            course_day = case_day(tmp_course_item[0:3])
            start_lesson, end_lesson = regx_lesson(tmp_course_item)
            classroom  = regx_classroom(tmp_course_item) if regx_classroom(tmp_course_item) else "无"
            wakeup_course_list.append({"课程名称": course["课程名称"], "星期": course_day, "开始节数": start_lesson, 
                                       "结束节数": end_lesson, "老师": course["老师"], "地点": classroom, "周数": course_week})
    return wakeup_course_list

def encryptPassword(password, key):
    # password 加密, 该段代码参考于 https://github.com/EdenLin-c/CPdaily/blob/master/Jin.py
    def randomString(len):
        retStr = ''
        i=0
        while i < len:
            retStr += aes_chars[(math.floor(random.random() * aes_chars_len))]
            i=i+1
        return retStr

    def getAesString(data,key,iv):
        key = re.sub('/(^\s+)|(\s+$)/g', '', key)
        aes = AES.new(str.encode(key),AES.MODE_CBC,str.encode(iv))
        pad_pkcs7 = pad(data.encode('utf-8'), AES.block_size, style='pkcs7')
        encrypted =aes.encrypt(pad_pkcs7)
        return str(base64.b64encode(encrypted),'utf-8')
    aes_chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678'
    aes_chars_len = len(aes_chars)
    encrypted = getAesString(randomString(64) + password, key, randomString(16))
    return encrypted


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

sso_response = session_client.post("https://ids.xidian.edu.cn/authserver/login", headers=headers, data=post_data, verify=False)
course_response = session_client.get("https://yjspt.xidian.edu.cn/yjsxkapp/sys/xsxkapp/xsxkCourse/loadKbxx.do", verify=False)
courses = json.loads(course_response.text)["xkjgList"]

tmp_wakeup_course_list = []

for course in courses:
    if "PKSJDD" in course:
        # 课程名称	星期	开始节数	结束节数	老师	地点	周数
        tmp_wakeup_course_list.append({"课程名称": course["KCMC"], "PKSJDD": course["PKSJDD"], "老师": course["RKJS"]})
wakeup_course_list =  parse_PKSJDD(tmp_wakeup_course_list)
print(wakeup_course_list)
dict_info = ["课程名称", "星期", "开始节数", "结束节数", "老师", "地点", "周数"]

with open('course.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = dict_info)
    writer.writeheader()
    writer.writerows(wakeup_course_list)
print("[+] Finish")