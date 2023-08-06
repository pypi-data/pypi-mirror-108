# -*- coding: utf-8 -*-
"""
     时间 : 2021-06-07 13:56
     作者 : 胡桓
     文件名 : myprint.py
     邮箱: 1641143982@qq.com
"""

import sys
import datetime

from testneo.log.settings import PRINT_COLOR, BG_COLOR

prefix_msg = '\033[1;{color}m{prefix}\033[0m'
detail_msg = '\033[1;{color}m{msg}\033[0m'
no_color_print = print


def color_print(self, *args, sep=' ', end='\n', file=None, color=PRINT_COLOR, bg_color=BG_COLOR):
    msg = repr(self) + sep + sep.join(repr(arg) for arg in args) + end
    line = sys._getframe().f_back.f_lineno
    file_name = sys._getframe(1).f_code.co_filename
    prefix = f'{datetime.datetime.now()} "{file_name}:{line}" '
    sys.stdout.write(prefix_msg.format(color=color, prefix=prefix))
    sys.stdout.write(detail_msg.format(color=bg_color, msg=msg))
    sys.stderr.flush()


def patch_print():
    try:
        __builtins__.print = color_print
    except AttributeError:
        __builtins__['print'] = color_print


def close_color_print():
    try:
        __builtins__.print = no_color_print
    except AttributeError:
        __builtins__['print'] = no_color_print