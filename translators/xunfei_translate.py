from datetime import datetime
from wsgiref.handlers import format_date_time
from time import mktime
import hashlib
import base64
import hmac
from urllib.parse import urlencode
import json
import requests

# 术语资源唯一标识，请根据控制台定义的RES_ID替换具体值，如不需术语可以不用传递此参数
RES_ID = "its_en_cn_word"
# 翻译原文本内容

class AssembleHeaderException(Exception):
    def __init__(self, msg):
        self.message = msg


class Url:
    def __init__(self, host, path, schema):
        self.host = host
        self.path = path
        self.schema = schema
        pass


# calculate sha256 and encode to base64
def sha256base64(data):
    sha256 = hashlib.sha256()
    sha256.update(data)
    digest = base64.b64encode(sha256.digest()).decode(encoding='utf-8')
    return digest


def parse_url(requset_url):
    stidx = requset_url.index("://")
    host = requset_url[stidx + 3:]
    schema = requset_url[:stidx + 3]
    edidx = host.index("/")
    if edidx <= 0:
        raise AssembleHeaderException("invalid request url:" + requset_url)
    path = host[edidx:]
    host = host[:edidx]
    u = Url(host, path, schema)
    return u


# build websocket auth request url
def assemble_ws_auth_url(requset_url, method="POST", api_key="", api_secret=""):
    u = parse_url(requset_url)
    host = u.host
    path = u.path
    now = datetime.now()
    date = format_date_time(mktime(now.timetuple()))
    # print(date)
    # date = "Thu, 12 Dec 2019 01:57:27 GMT"
    signature_origin = "host: {}\ndate: {}\n{} {} HTTP/1.1".format(host, date, method, path)
    # print(signature_origin)
    signature_sha = hmac.new(api_secret.encode('utf-8'), signature_origin.encode('utf-8'),
                             digestmod=hashlib.sha256).digest()
    signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')
    authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
        api_key, "hmac-sha256", "host date request-line", signature_sha)
    authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
    # print(authorization_origin)
    values = {
        "host": host,
        "date": date,
        "authorization": authorization
    }

    return requset_url + "?" + urlencode(values)


url = 'https://itrans.xf-yun.com/v1/its'

class XunfeiTranslator:
    def __init__(self,cfg=None):
        self.APPId=''
        self.APISecret=''
        self.APIKey=''
        if cfg:
            try:
                self.APPId = cfg['讯飞']['APPId']
                self.APISecret = cfg['讯飞']['APISecret']
                self.APIKey = cfg['讯飞']['APIKey']
            except:
                print('讯飞翻译载入失败')
    
    def config(self,cfg):
        try:
            self.APPId = cfg['讯飞']['APPId']
            self.APISecret = cfg['讯飞']['APISecret']
            self.APIKey = cfg['讯飞']['APIKey']
        except:
            print('讯飞翻译载入失败')
    
    def translate(self,in_str,fromLang='en',toLang='cn')->str:
        body = {
            "header": {
                "app_id": self.APPId,
                "status": 3,
                "res_id": RES_ID
            },
            "parameter": {
                "its": {
                    "from": fromLang,
                    "to": toLang,
                    "result": {}
                }
            },
            "payload": {
                "input_data": {
                    "encoding": "utf8",
                    "status": 3,
                    "text": base64.b64encode(in_str.encode("utf-8")).decode('utf-8')
                }
            }
        }

        request_url = assemble_ws_auth_url(url, "POST", self.APIKey, self.APISecret)

        headers = {'content-type': "application/json", 'host': 'itrans.xf-yun.com', 'app_id': self.APPId}
        # print(request_url)
        try:
            response = requests.post(request_url, data=json.dumps(body), headers=headers)
            tempResult = json.loads(response.content.decode())
            temp = base64.b64decode(tempResult['payload']['result']['text']).decode()
            temp = json.loads(temp)
            out = temp['trans_result']['dst']
        except:
            out='error'
        finally:
            return out

if __name__=='__main__':
    with open('../test.json','r',encoding='utf-8') as f:
        cfg = json.load(f)
    translator = XunfeiTranslator(cfg)
    print(translator.translate('apple'))
