# *_* coding : UTF-8 *_*
# author  ：  Leemamas
# 开发时间  ：  2021/6/8  8:42
import setuptools
with open("README.md", "r") as f:
    long_description = f.read()
setuptools.setup(
    name="tablepet",  # 模块名称
    version="1.0",  # 当前版本
    author="dml",  # 作者
    author_email="kkleung88@gmali.com",  # 作者邮箱
    description="桌面宠物",  # 模块简介
    long_description=long_description,  # 模块详细介绍
    long_description_content_type="text/markdown",  # 模块详细介绍格式
    url="https://github.com/leemams/godtoy",  # 模块github地址
    packages=setuptools.find_packages(),  # 自动找到项目中导入的模块
    # 模块相关的元数据
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # 依赖模块
    install_requires=[
        'pyqt5',
    ],
    python_requires='>=3',
)