import requests, uuid, json

endpoint = "https://api.cognitive.microsofttranslator.com"

# location, also known as region.
# required if you're using a multi-service or regional (not global) resource. It can be found in the Azure portal on the Keys and Endpoint page.

path = '/translate'
constructed_url = endpoint + path

class MicrosoftTranslator:
    def __init__(self,cfg=None):
        self.key=''
        self.location=''
        if cfg:
            try:
                self.key = cfg['微软']['key']
                self.location = cfg['微软']['location']
            except:
                print('加载微软翻译配置失败')
    
    def config(self,cfg):
        try:
            self.key = cfg['微软']['key']
            self.location = cfg['微软']['location']
        except:
            print('加载微软翻译配置失败')
    
    def translate(self,in_str, fromLang='auto',toLang='zh-CHS')->str:
        params = {
            'api-version': '3.0',
            'from': 'en',
            'to': ['zh-CHS']
        }

        headers = {
            'Ocp-Apim-Subscription-Key': self.key,
            # location required if you're using a multi-service or regional (not global) resource.
            'Ocp-Apim-Subscription-Region': self.location,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        # You can pass more than one object in body.
        body = [{
            'text': in_str
        }]
        out = ''
        try:
            request = requests.post(constructed_url, params=params, headers=headers, json=body)
            response = request.json()
            #print(response)
            out = response[0]['translations'][0]['text']
        except:
            out='error'
        finally:
            return out

if __name__=='__main__':
    with open('../test.json','r',encoding='utf-8') as f:
        cfg = json.load(f)
    translator = MicrosoftTranslator(cfg)
    print(translator.translate('apple'))