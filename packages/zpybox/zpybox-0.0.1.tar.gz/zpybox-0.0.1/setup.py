# coding:utf-8

from setuptools import setup

def get_ver_from_readme(readme_path):
    with open("README.md", "r", encoding='utf-8') as fs:
        for line in fs.readlines():
            if "当前版本：" in line:
                return line.split("：")[1]
    exit(0)

with open("README.md", "r", encoding='utf-8') as fs:
    long_description = fs.read()


cur_ver = get_ver_from_readme("README.md")

setup(
    name = 'zpybox',
    version = cur_ver,
    author = 'ZF',
    author_email = 'zofon@qq.com',
    description = "python tool box in Chinese",
    packages=[
        "zpybox",
        ],
    # py_module=[""]
    long_description = long_description,
    long_description_content_type="text/markdown",

    platforms = ["windows or Linux"],
    keywords = ['tool'],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires=">=2.7.5",
    # install_requires=[
    #     "netmiko>=2.0.0",
    # ],
)