# -*- coding:utf-8 -*-
#__author = zhangguohua02

import time
import os
import os.path
import shutil
import re
from pprint import pprint


def copy_fileto(src, dst_dir):
    shutil.copy(src, dst_dir)

def getCurrentTime():
    nowTime = time.localtime()
    year = str(nowTime.tm_year)
    month = str(nowTime.tm_mon)
    day = str(nowTime.tm_mday)
    hour = str(nowTime.tm_hour)
    min = str(nowTime.tm_min)
    sec = str(nowTime.tm_sec)
    if len(month) < 2:
        month = '0' + month
    if len(day) < 2:
        day = '0' + day
    if len(sec) < 2:
        sec = '0' + sec
    return year + '-' +  month + '-' + day + '-' + hour + '-' + min + '-' + sec


"""
search_dir is the search directory, the function will search the subdirectory too.
fileName is the key, the function support regular express when searching.
copy_dir is the directory which matched-file will copy into.
"""
def search_and_copy_file_by_name(search_dir, file_name, copy_dir):
    if not os.path.exists(search_dir):
        print 'search_dir not exit'
        retunr -1
    print 'begin'
    result = []
    for file in os.listdir(search_dir):
        print file
        #print
        result.append(file)
        src_file = os.path.join(search_dir, file)
        #print target_file
        #print os.path.isfile(target_file)
        exclude = '.*?(uvoptx|uvprojx)$'
        if os.path.isfile(src_file) and re.match(file_name, file) and not re.match(exclude, src_file):
            if not os.path.exists(copy_dir):
               os.makedirs(copy_dir)

            dst_file = os.path.join(copy_dir, file)
            #print dst_file
            #print os.path.isfile(dst_file)
            try:
                if os.path.exists(src_file) and os.path.isfile(src_file):
                    #print os.path.getsize(src_file)
                    if not os.path.exists(dst_file) or (os.path.exists(dst_file) and os.path.getsize(src_file) !=
                    os.path.getsize(dst_file) ):
                        #print dst_file
                        #print src_file
                        open(dst_file, "wb").write(open(src_file,"rb").read())
            except OSError:
                print src_file + ' error'
                return -2
        if os.path.isdir(src_file):
            sec_val = search_and_copy_file_by_name(src_file, file_name, copy_dir)
            result.append(sec_val)
        #print result
        return result

"""
remove the files which match the 'key' in regular express in the dir
"""
def remove_file(dir, key):
    if not os.path.exists(dir):
        print 'dir not exit'
        return -1
    for file in os.listdir(dir):
        #print file
        if re.match(key, file):
            remove_file = os.path.join(dir, file)
            os.remove(remove_file)

def list_dir(src_dir, ret_val):
    result = []
    for file in os.listdir(src_dir):
        result.append(file)
        ret_val.append(file)
    print result
    return result

if __name__ == "__main__":
    dirTime = getCurrentTime()
    src_dir = 'E:\\ref\\python\\IoTImage\\projects'
    src = 'E:\\ref\\python\\IoTImage\\projects\\clean-obj.py'
    copy_dir = 'E:\\ref\\python\\IoTImage' + dirTime
    #print copy_dir
    val = search_and_copy_file_by_name(src_dir, 'uv4_log|TinyDu*', copy_dir)
    print val
    #remove_file(copy_dir, '.*?(uvoptx|uvprojx|BAT|bat)$')
    #try:
    #print copy_fileto(src,'E:\\ref\\python')
    #except IOError:
    print 'move file to IOerror'
    #val = ()
    #print list_dir(src_dir, val)

    #print 'after val: ', val
