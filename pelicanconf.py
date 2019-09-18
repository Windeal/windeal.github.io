#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Windeal'
SITENAME = 'Windeal\'s Home'
SITEURL = ''

PATH = 'content'
STATIC_PATHS = ['hello', 'extra']

EXTRA_PATH_METADATA = {
#            'static/robots.txt': {'path': 'robots.txt'},
            'extra/CNAME': {'path': 'CNAME'},
        }

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = 'zh'
SUMMARY_MAX_LENGTH = 50




# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None


# 插件
PLUGIN_PATHS = ["plugins", "plugins"]
PLUGINS = ["related_posts", "neighbors"]

RELATED_POSTS_MAX = 10 

#Theme ==== 主题
THEME = './theme/octopress'

# 导航栏
BOOTSTRAP_NAVBAR_INVERSE = True
DISPLAY_CATEGORIES_ON_MENU = False          #导航栏显示文章类别
DISPLAY_ARCHIVES_ON_MENU = True
MENUITEMS = (   
                ('我的博客', '/'),  
                ('分类目录', '/categories.html'),
                ('关于博主', '/pages/aboutme.html'), 
            )

MY_CATEGORY_MAP = {
        "bugs":("Bugs收录", ""),
        "tcpip":("TCPIP协议", ""),
        "tools":("工具与环境", ""),
        "unixcoding":("Unix环境编程", ""),
        "background":("后台开发", ""),
        "protocol":("协议", "")
        } 
