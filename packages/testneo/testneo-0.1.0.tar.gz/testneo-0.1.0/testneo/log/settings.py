# -*- coding: utf-8 -*-
"""
     时间 : 2021-06-01 10:14
     作者 : 胡桓
     文件名 : settings.py
     邮箱: 1641143982@qq.com
"""

WHITE = 30  # 白色
RED = 31  # 红色
GREEN = 32  # 绿色
YELLOW = 33  # 黄色
BLUE = 34  # 蓝色
PURPLE = 35  # 紫色
BABYBLUE = 36  # 浅蓝色
GREY = 37  # 灰色
FrenchGREY = 38  # 浅灰色

PRINT_COLOR = BLUE
BG_COLOR = GREEN

default_config = {
    'level': 'INFO',
    'name': 'root',
    'formatter': '[%(levelname)s - %(asctime)s - %(name)s - %(filename)s - line:%(lineno)d] %(message)s',
    'file': 'testneo.log',
    'error_color': RED,
    'warning_color': YELLOW,
    'info_color': WHITE,
    'debug_color': GREEN,
    'is_color_print':True,
}
