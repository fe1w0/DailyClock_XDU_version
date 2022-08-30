# Author: fe1w0
import requests
import traceback
import sys

proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
    }

class SSO:
    # 单点登录
    username = ""
    password = ""
    requests_url = ""
    
    def __init__(self, username, password, url="https://xxcapp.xidian.edu.cn/uc/wap/login/check"):
        self.username = username
        self.password = password
        self.requests_url = url
        
    def create_client(self):
        session_client = requests.Session()
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54"
        }
        post_data = {
            "username": self.username,
            "password": self.password
        }
        requests.packages.urllib3.disable_warnings()
        try:
            response = requests.post(url=self.requests_url, data=post_data, headers=headers, verify=False)
            if "操作成功" not in response.text:
                print("[!] Fail to login sso server")
                sys.exit(0)
        except:
            print("[!] Fail to login sso server")
            traceback.print_exc()
            sys.exit(0)
        return requests.utils.dict_from_cookiejar(response.cookies)
    

class Clock:
    post_form = None
    session_client = None
    xidiandailyup_requests_url = ""
    headers = None
    
    
    def __init__(self, session_client, xidiandailyup_requests_url="https://xxcapp.xidian.edu.cn/xisuncov/wap/open-report/save"):
        self.xidiandailyup_requests_url = xidiandailyup_requests_url
        self.session_client = session_client
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54"
        }
        
        self.post_form = {
            "sfzx": 1,
            "tw": 2,
            "area": "浙江省 杭州市 萧山区",
            "city": "杭州市",
            "province": "浙江省",
            "address": "浙江省杭州市萧山区宁围街道萧清大道",
            "geo_api_info": '{"type":"complete","position":{"Q":30.235995551216,"R":120.32076307508703,"lng":120.320763,"lat":30.235996},"location_type":"html5","message":"Get ipLocation failed.Get geolocation success.Convert Success.Get address success.","accuracy":35,"isConverted":true,"status":1,"addressComponent":{"citycode":"0571","adcode":"330109","businessAreas":[],"neighborhoodType":"","neighborhood":"","building":"","buildingType":"","street":"萧清大道","streetNumber":"27号2栋","country":"中国","province":"浙江省","city":"杭州市","district":"萧山区","towncode":"330109014000","township":"宁围街道"},"formattedAddress":"浙江省杭州市萧山区宁围街道萧清大道","roads":[],"crosses":[],"pois":[],"info":"SUCCESS"}',
            "sfcyglq": 0,
            "sfyzz": 0,
            "qtqk": None,
            "ymtys": 0
        }
    
    def xidiandailyup_clock(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54"
        }
        try:
            response = requests.post(url=self.xidiandailyup_requests_url, data=self.post_form, cookies=self.session_client, headers=self.headers, verify=False)
            if "操作成功" not in response.text and "您已上报过" not in response.text:
                print("[!] Fail to clock xidiandailyup")
                print(response.text)
                return False
        except:
            print("[!] Fail to clock xidiandailyup")
            traceback.print_exc()
            sys.exit(0)
        return True
    
