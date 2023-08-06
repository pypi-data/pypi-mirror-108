# -*- coding: utf-8 -*-
"""
     时间 : 2021-05-28 16:27
     作者 : 胡桓
     文件名 : __init__.py.py
     邮箱: 1641143982@qq.com
"""

from __future__ import absolute_import

from testneo.log.myprint import no_color_print,color_print,patch_print,close_color_print
from testneo.log.settings import *

__all__ = ['no_color_print','color_print','patch_print']

if default_config.get('is_color_print'):
    patch_print()
else:
    close_color_print()