# -*- coding: UTF-8 -*-

import sys
import time

def get_cur_datetime():
    # 时间定义，用生成文档的名字
    # curDateTime = time.strftime('%Y-%m-%d %H-%M-%S',time.localtime(time.time()))
    curDateTime = time.strftime('%Y%m%d %H%M',time.localtime(time.time()))
    curDate = curDateTime.split(" ")[0]
    curTime = curDateTime.split(" ")[1]
    return(curDate,curTime)


def get_time_stamp(format="YYYYMMDDHHMMSS"):
    if format == "YYYYMMDDHHMMSS":
        return time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    elif format == "YYYYMMDDHHMM":
        return time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
    elif format == "YYYYMMDDHH":
        return time.strftime('%Y%m%d%H', time.localtime(time.time()))
    elif format == "YYYYMMDD":
        return time.strftime('%Y%m%d', time.localtime(time.time()))
    elif format == "YYYYMM":
        return time.strftime('%Y%m', time.localtime(time.time()))
    elif format == "YYYY":
        return time.strftime('%Y', time.localtime(time.time()))
    else:
        return time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))


if __name__ == '__main__':
    sys.exit(0)
