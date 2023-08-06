# coding:utf-8

from setuptools import setup

with open("README.md", "r", encoding='utf-8') as fs:
    long_description = fs.read()

setup(
    name = 'ibnsession',
    version = '1.3.2',
    author = 'ZF',
    author_email = 'zofon@qq.com',
    description = "Library for IBN",
    packages=[
        "ibnsession",
        "ibnsession/core",
        "ibnsession/tool",
        ],
    # py_module=[""]
    long_description = long_description,
    long_description_content_type="text/markdown",

    platforms = ["windows or Linux"],
    keywords = ['ibn', 'ops'],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires=">=2.7.5",
    install_requires=[
        "netmiko>=2.0.0",
    ],
)

