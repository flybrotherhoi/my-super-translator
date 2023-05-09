import json
import requests

url = "http://api.interpreter.caiyunai.com/v1/translator"

# WARNING, this token is a test token for new developers,
# and it should be replaced by your token

class CaiyunTranslator:
    def __init__(self,cfg=None):
        self.token=''
        if cfg:
            try:
                self.token = cfg['彩云']['token']
            except:
                print('加载彩云翻译配置失败')
    
    def config(self,cfg):
        try:
            self.token = cfg['彩云']['token']
        except:
            print('加载彩云翻译配置失败')

    def translate(self,source, direction="auto2zh"):
        try:
            payload = {
                "source": source,
                "trans_type": direction,
                "request_id": "demo",
                "detect": True,
            }

            headers = {
                "content-type": "application/json",
                "x-authorization": "token " + self.token,
            }
        
            response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
            out=json.loads(response.text)["target"]
        except:
            out='error'
        finally:
            return out

if __name__=="__main__":
    with open('../test.json','r',encoding='utf-8') as f:
        cfg = json.load(f)
    translator = CaiyunTranslator(cfg)
    print(translator.translate('apple'))