# -*- coding: UTF-8 -*-

import sys

def power_print(str):
    py_version = (sys.version).split(".")[0]
    if py_version == '3':
        eval("print(str)")
    elif py_version == '2':
        eval("print str")
    else:
        raise Exception("python version ERROR:" + sys.version)
    return True


def show_debug_info(str):
    return power_print(str)


def write_into_new_file(file_name, time_stamp='NULL', mode='a'):
    if time_stamp == "NULL":
        import time
        time_stamp = str(int(time.time() * 1000))
        time.sleep(0.001)  # 进行毫秒级控制，在普通的计算机上面运行，这句话可以不要
    file_name = time_stamp + "_" + file_name
    with open(file_name, mode) as file_object:
        file_object.write("Add a word")


def write_into_file(file_name, writing_strings, mode='a'):
    if isinstance(writing_strings, str):
        with open(file_name, mode) as file_object:
            file_object.write(writing_strings)
        return True
    elif isinstance(writing_strings, list):
        with open(file_name, mode) as file_object:
            for line in writing_strings:
                file_object.write(line + "\n")
        return True
    else:
        return False



def print_list(List):
    for line in List:
        print(line,end="")

def printList(List):
    return print_list(List)


if __name__ == '__main__':
    write_into_file("test.txt", "HI")
    writing_strings = ["EE", "AA"]
    write_into_file("test1.txt", writing_strings)