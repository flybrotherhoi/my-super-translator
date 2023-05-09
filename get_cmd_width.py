#-*- coding:utf-8 -*-

from ctypes import windll, create_string_buffer
import struct

def get_cmd_width()->int:
    
    win_stdout = -11

    fd = windll.kernel32.GetStdHandle(win_stdout)

    #获得标准输出的句柄

    cstruct = create_string_buffer(22)

    rc_struct = windll.kernel32.GetConsoleScreenBufferInfo(fd, cstruct)

    #获得控制台的属性
    sizex=80
    if rc_struct:


        (bufx, bufy, curx, cury, wattr,
         left, top, right, bottom, maxx, maxy) = struct.unpack("hhhhHhhhhhh", cstruct)

        sizex = right - left + 1

        sizey = bottom - top + 1

    return sizex

if __name__=='__main__':
    print(get_cmd_width())