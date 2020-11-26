# %%
import re
import os
import requests
import logging
import sys
import time
import warnings
import random
import requests
from requests.exceptions import RequestException
import time
import json
# %%
warnings.filterwarnings('ignore') #ignore std warning，don't mind

domain ='https://gkdworld.xyz/'
signURL = os.environ["SIGNURL"].split(" ")
myCookie= os.environ["COOKIE"].split(" ")
SREVERCHAN= os.environ["SREVERCHAN"]
HEADER = {
    "user-agent":
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
    "dnt": "1",
}

PROXY = {
    "http": "http://127.0.0.1:1080",
    "https": "http://127.0.0.1:1080"
}

RETRY_NUM = 5

try:
    import brotli
    HEADER["accept-encoding"] = "gzip, deflate, br"
except ImportError as e:
    HEADER["accept-encoding"] = "gzip, deflate"

# %%
def get_randint(min_num, max_num):
    if min_num > max_num:
        raise ValueError("Illegal arguments...")
    return random.randint(min_num, max_num)


def extract_domain(url):
    if not url:
        return ""

    start = url.find("//")
    if start == -1:
        start = -2

    end = url.find("/", start + 2)
    if end == -1:
        end = len(url)

    return url[start + 2:end]

def is_checked(url):
    flag = False
    return flag

def get_formhash():
    # TODO, how?
    pass

def checkin(url, headers, form_data, retry, proxy=False):
    def has_checked(url):
        logging.info("已经签到 URL: {}".format(extract_domain(url)))
        print("已签{}".format(extract_domain(url)))
        return 
    def success(url):
        logging.info("签到成功 URL: {}".format(extract_domain(url)))
        print("成功{}".format(extract_domain(url)))
        requests.get("https://sc.ftqq.com/"+SREVERCHAN+".send?text={}{}".format("成功",extract_domain(url)))
        return
    def cookie_err(url):
        logging.error("签到失败 URL: {}, cookies或formhash过期".format(extract_domain(url)))
        print("非法失败{}".format(extract_domain(url)))
        text = "{}, 签到出现非法失败, 手动更新cookies或formhash".format(extract_domain(url))
        requests.get("https://sc.ftqq.com/"+SREVERCHAN+".send?text={}".format(text))
        return
    def failed(url):
        logging.error("签到失败 URL: {}, 未知错误".format(extract_domain(url)))
        print("未知失败{}".format(extract_domain(url)))
        text = "{}, 签到出现未知失败".format(extract_domain(url))
        requests.get("https://sc.ftqq.com/"+SREVERCHAN+".send?text={}".format(text))
        print(text)
        return
    
    checkin_dict = {
        "已签|已经签到|签过到": has_checked,
        "签到成功": success,
        "未定义|非法": cookie_err,
    }

    try:
        if proxy:
            response = requests.post(url, headers=headers, proxies=PROXY, verify=False)
        else:
            response = requests.post(url, headers=headers, data=form_data)
        # print("+++++++++++++++++++++++++++")
        # print(response.text)
        if response.status_code == 200:
            flag = False
            for key in checkin_dict:
                if re.findall(key, response.text) != []:
                    flag = True
                    checkin_dict[key](url)
            if flag == False:
                failed(url)
            return 

    except RequestException as e:
        logging.error(str(e))
        retry -= 1

        if retry > 0:
            time.sleep(get_randint(30, 60 * 60))
            checkin(url, headers, retry, proxy)

        logging.error(u"签到失败 URL: {}".format(extract_domain(url)))

def flow(domain, params, headers, checkin_url, proxy=False):
    domain = domain.strip()# remvoe space in start and tail
    regex = "(?i)^(https?:\\/\\/)?(www.)?([^\\/]+\\.[^.]*$)"
    flag = re.search(regex, domain)

    if not flag:
        return False

    cookie = params["cookies"]
    headers["cookie"] = cookie
    form_data = {}
    headers["origin"] = domain
    if not is_checked(domain):
        checkin(checkin_url, headers, form_data, RETRY_NUM, proxy)
    else:
        logging.info("已经签到 URL: {}".format(extract_domain(domain)))

def wrapper(args):
    flow(args["domain"], args["param"], HEADER, args["checkin_url"], args["proxy"])

if __name__ == '__main__':
    idx = 0
    for c in myCookie:
        signdata = {"domain":domain,"param":{"cookies":c},'checkin_url':signURL[idx],'proxy':False}
        wrapper(signdata)
        idx  = idx +1
