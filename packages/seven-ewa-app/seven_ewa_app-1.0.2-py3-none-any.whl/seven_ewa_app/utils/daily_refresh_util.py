# -*- coding:utf-8 -*-
"""
:Author: SunYiTan
:Date: 2020/7/22 16:48
:LastEditTime: 2020/7/22 16:48
:LastEditors: SunYiTan
:Description: 当天刷新时间工具类
"""

from datetime import datetime


class DailyRefreshUtil:

    @staticmethod
    def get_today_refresh_time(refresh_time):
        now = datetime.now()
        today_refresh_time = int(now.replace(hour=int(refresh_time / 10000), minute=int(refresh_time % 10000 // 100),
                                             second=int(refresh_time % 100), microsecond=0).timestamp())
        if int(now.timestamp()) < today_refresh_time:
            today_refresh_time -= 24 * 60 * 60

        return today_refresh_time
