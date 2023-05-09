# coding=utf-8
import http.client
import hashlib
import urllib
import random
import json

class BaiduTranslator:
    def __init__(self,cfg=None):
        self.appid=''
        self.secretKey=''
        if cfg:
            try:
                self.appid = cfg['百度']['appid']
                self.secretKey = cfg['百度']['secretKey']
            except:
                print('加载百度翻译配置失败')
    
    def config(self,cfg):
        try:
            self.appid = cfg['百度']['appid']
            self.secretKey = cfg['百度']['secretKey']
        except:
            print('加载百度翻译配置失败')

    def translate(self,in_str,fromLang='auto',toLang='zh')->str:
        '''
        Return:
        translated str\n\n

        Args:\n
        in_str: 待翻译字符串\n
        fromLang = 'auto' 原文语种\n
        toLang = 'zh' 译文语种
        '''
        httpClient = None
        myurl = '/api/trans/vip/translate'

        salt = random.randint(32768, 65536)
        sign = self.appid + in_str + str(salt) + self.secretKey
        sign = hashlib.md5(sign.encode()).hexdigest()
        myurl = myurl + '?appid=' + self.appid + '&q=' + urllib.parse.quote(in_str) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign

        out_str = ''
        try:
            httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
            httpClient.request('GET', myurl)

            # response是HTTPResponse对象
            response = httpClient.getresponse()
            result_all = response.read().decode("utf-8")
            result = json.loads(result_all)
            out_str = result['trans_result'][0]['dst']
            #print (result)

        except Exception as e:
            #print (e)
            out_str='error'
        finally:
            if httpClient:
                httpClient.close()
            return out_str
    
if __name__=='__main__':
    with open('../test.json','r',encoding='utf-8') as f:
        cfg = json.load(f)
    translator = BaiduTranslator(cfg)
    print(translator.translate('apple'))
