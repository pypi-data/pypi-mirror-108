# -*- coding: UTF-8 -*-

import sys

from .output import print_list

def check_file_exist(files, debug_mode = False):
    from os.path import isfile
    if isinstance(files,list):
        if debug_mode == True :
            print("检查多个文件:")
            print_list(files)
        for file in files:                                                     # 如果文件均检查正常，则返回 True
            if isfile(file):
                pass
            else:
                if debug_mode == True : print("{} 文件不存在，或者不是一个文件".format(file))
                return False
        return True
    elif isinstance(files,str):
        if debug_mode == True : print("检查单个文件")
        if isfile(files):
            return True
        else:
            if debug_mode == True: print("{} 文件不存在，或者不是一个文件".format(files))
            return False
    else:
        if debug_mode == True: print("传入的参数，既不是列表也不是字符串，无法进行文件检查")
        return False


def markdown_to_html(markdown_file_path, html_file_path, debug_mode = True):
    """
    :param markdown_file_path: =
    :param html_file_path: =
    :param debug_mode: =
    :return: =
    """
    import codecs, markdown
    if debug_mode == True : print("读取 markdown 文本")
    input_file = codecs.open(markdown_file_path, mode="r", encoding="utf-8")
    text = input_file.read()
    if debug_mode == True : print("转为 html 文本")
    html = markdown.markdown(text)
    if debug_mode == True : print("保存为文件")
    output_file = codecs.open(html_file_path, mode="w", encoding="utf-8")
    output_file.write(html)


if __name__ == '__main__':
    sys.exit(0)
