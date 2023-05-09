
# -*- coding: utf-8 -*-
import sys
import uuid
import requests
import hashlib
import time
import json

YOUDAO_URL = 'https://openapi.youdao.com/api'

def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()

def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]

def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)

class YoudaoTranslator:
    def __init__(self,cfg=None):
        self.APPId = ''
        self.APPSecret = ''
        if cfg:
            try:
                self.APPId = cfg['有道']['APPId']
                self.APPSecret = cfg['有道']['APPSecret']
            except:
                print('加载有道翻译配置失败')
    
    def config(self,cfg):
        try:
            self.APPId = cfg['有道']['APPId']
            self.APPSecret = cfg['有道']['APPSecret']
        except:
            print('加载有道翻译配置失败')
            
    def translate(self,in_str, fromLang='auto',toLang='zh-CHS')->str:
        q=in_str
        data = {}
        data['from'] = fromLang
        data['to'] = toLang
        data['signType'] = 'v3'
        curtime = str(int(time.time()))
        data['curtime'] = curtime
        salt = str(uuid.uuid1())
        signStr = self.APPId + truncate(q) + salt + curtime + self.APPSecret
        sign = encrypt(signStr)
        data['appKey'] = self.APPId
        data['q'] = q
        data['salt'] = salt
        data['sign'] = sign
        #data['vocabId'] = "您的用户词表ID"
        out=''
        try:
            response = do_request(data)
            out = response.json()['translation'][0]
        except:
            out='error'
        finally:
            return out

if __name__ == '__main__':
    with open('../test.json','r',encoding='utf-8') as f:
        cfg = json.load(f)
    translator = YoudaoTranslator(cfg)
    print(translator.translate('apple'))