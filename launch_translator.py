import pynput.mouse as mouse
import pynput.keyboard as keyboard
import pyperclip
import colorama
import argparse
import os,time
import json
from translators import *
from get_cmd_width import get_cmd_width


debug = 0
colorama.init(autoreset=True)
global go_to_die
go_to_die=False
def content_format(content):
    out = content.replace('\r\n', ' ')
    return out

key_controller = keyboard.Controller()

def on_mouse_click(x, y, button, pressed):
    # 选中翻译，此函数弃用，这样太浪费资源
    global last_x,last_y,content,last_content
    if (not pressed) and button==mouse.Button.left and not (last_x==x and last_y==y):
        with key_controller.pressed(keyboard.Key.ctrl):
            key_controller.press('c')
            time.sleep(0.01)
            key_controller.release('c')
        #time.sleep(0.1) # 在adobe的pdf阅读器里，复制貌似有点问题
        content = content_format(pyperclip.paste())
        if last_content!=content and do_translate:
            print(
f'''===============================【{curr_engine}翻译】===============================
原文：\033[93m{content}\033[0m
..........................................................................
译文：\033[92m{translators[curr_engine](content)}\033[0m
==========================================================================
'''
                )
            last_content = content
    if pressed and button==mouse.Button.left:
        last_x,last_y = (x,y)
    
def on_key_release(key):
    global go_to_die
    if go_to_die:
        return False

def on_activate_h():
    cw = get_cmd_width()
    hcw = int(cw/2)-3
    print(hcw*'=','HELP',hcw*'=')
    print('''
                    \033[92mCtrl+Alt+H\033[0m：  查看帮助
                    \033[92mCtrl+Alt+Q\033[0m：  退出软件
                
                    \033[92mCtrl+Alt+i\033[0m：  暂停/开始选中翻译
                
                    \033[92mCtrl+Alt+1\033[0m：  切换到【\033[95m百度翻译\033[0m】引擎
                    \033[92mCtrl+Alt+2\033[0m：  切换到【\033[95m微软翻译\033[0m】引擎
                    \033[92mCtrl+Alt+3\033[0m：  切换到【\033[95m彩云翻译\033[0m】引擎
                    \033[92mCtrl+Alt+4\033[0m：  切换到【\033[95m讯飞翻译\033[0m】引擎
                    \033[92mCtrl+Alt+5\033[0m：  切换到【\033[95m有道翻译\033[0m】引擎
                    
                    \033[91m如遇到翻译结果为error，可以尝试关掉代理\033[0m
            ''')
    print(cw*'=')
    print()

def on_activate_1():
    global curr_engine
    curr_engine = trans_engines[0]
    print('当前翻译引擎:',curr_engine)

def on_activate_2():
    global curr_engine
    curr_engine = trans_engines[1]
    print('当前翻译引擎:',curr_engine)

def on_activate_3():
    global curr_engine
    curr_engine = trans_engines[2]
    print('当前翻译引擎:',curr_engine)

def on_activate_4():
    global curr_engine
    curr_engine = trans_engines[3]
    print('当前翻译引擎:',curr_engine)

def on_activate_5():
    global curr_engine
    curr_engine = trans_engines[4]
    print('当前翻译引擎:',curr_engine)


def on_activate_i():
    global do_translate
    do_translate = not do_translate
    if do_translate:
        print('选中翻译已开始')
    else:
        print('选中翻译已暂停')

def on_activate_c():
    #key_controller.release(keyboard.Key.alt)
    with key_controller.pressed(keyboard.Key.ctrl):
        key_controller.press('c')
        time.sleep(0.01)
        key_controller.release('c')
    #time.sleep(0.1) # 在adobe的pdf阅读器里，复制貌似有点问题
    content = content_format(pyperclip.paste())
    #print(content)
    if do_translate:
        cw=get_cmd_width()
        hcw = int(cw/2)-7
        c = '`'
        print(c*hcw,f'【{curr_engine}翻译】',c*hcw)
        print(f'原文：\033[93m{content}\033[0m')
        print('.'*cw)
        print(f'译文：\033[92m{translators[curr_engine].translate(content)}\033[0m')
        print(c*cw)
        print()

def on_activate_q():
    global go_to_die
    go_to_die=True


global last_x,last_y
last_x = 0
last_y = 0
go_to_die=False
global content,last_content
content = ''
last_content = ''

global curr_engine, do_translate
curr_engine = '百度'    # 默认是百度
trans_engines = ['百度','微软','彩云','讯飞','有道']
translators = {
    '百度': BaiduTranslator(),
    '有道': YoudaoTranslator(),
    '微软': MicrosoftTranslator(),
    '讯飞': XunfeiTranslator(),
    '彩云': CaiyunTranslator()
}
do_translate=True



# ===========================main==================================

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="我的超级翻译器传入配置参数")
    parser.add_argument('--config',type=str,default='default.json',help='指定各翻译引擎API的配置文件，默认为default.json')
    
    args = parser.parse_args()
    config_path = args.config

    try:
        with open(config_path,'r',encoding='utf-8') as f:
            cfg = json.load(f)
    except:
        print('配置文件加载失败！')
        i=5
        while i>-1:
            print('\r',i,"秒后退出",end='')
            i-=1
            time.sleep(1)
        exit()
        
    for trans in translators:
        translators[trans].config(cfg)
    
    cw = get_cmd_width()
    print('='*cw)
    print('''
    欢迎使用\033[95m我的超级翻译器\033[0m，作者：\033[96mflybrotherhoi\033[0m
    
    使用方法：选中文字后按\033[92m Ctrl+C \033[0m进行翻译，翻译结果在此窗口下。
                                     
    温馨提示：使用过程中按\033[92m Ctrl+Alt+H \033[0m可以查看帮助，按\033[92m Ctrl+Alt+Q \033[0m退出。 
    ''')
    print('='*cw)
    print()

    esc_listener = keyboard.Listener(on_release=on_key_release)
    esc_listener.start()
    
    hotkey_listener = keyboard.GlobalHotKeys({
        '<ctrl>+<alt>+h':on_activate_h,
        '<ctrl>+<alt>+1':on_activate_1,
        '<ctrl>+<alt>+2':on_activate_2,
        '<ctrl>+<alt>+3':on_activate_3,
        '<ctrl>+<alt>+4':on_activate_4,
        '<ctrl>+<alt>+5':on_activate_5,
        '<ctrl>+<alt>+i':on_activate_i,
        '<ctrl>+<alt>+q':on_activate_q,
        '<ctrl>+c':on_activate_c
    })
    hotkey_listener.start()

    esc_listener.join()
    hotkey_listener.stop()
    
    print('='*get_cmd_width())
    print('''
          \033[95m感谢使用，祝你一切顺利！ \033[0m
          ''')
    print('='*get_cmd_width())
    time.sleep(0.5)
    print('')