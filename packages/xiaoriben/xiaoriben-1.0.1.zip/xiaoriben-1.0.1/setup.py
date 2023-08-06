# 项目信息的配置文件
# 这里面最重要一个就是执行setup函数，通过这个函数来指明信息
# from distutils.core import setup
from setuptools import setup


def readme_file():
    with open('README.rst', encoding='utf-8') as rf:
        return rf.read()


setup(name='xiaoriben', version='1.0.1', description='this is a niubi lib2',
      packages=['sztestlib'], py_modules=['dos'], author='Sz', author_email='651757088@qq.com',
      long_description=readme_file(), url='http://upload.pypi.org/legacy/', license='MIT')
