# -*- coding:utf-8 -*-
"""
:Author: SunYiTan
:Date: 2021/5/19 12:04
:LastEditTime: 2021/5/19 12:04
:LastEditors: SunYiTan
:Description: 
"""

from enum import Enum, unique


class AppBaseRedisKeyType(Enum):
    """
    redis用到的key
    """
    QqAccessToken = "qq_access_token:"  # QQ accessToken
    QqAccessTokenLock = "qq_access_token_lock:"  # QQ accessToken
    UserToken = "pt_app_user_token:"
    ThirdToken = "pt_app_third_token:"
