@ECHO off
ECHO Installing Pipenv, If fails, please install python 3.10
ECHO 正在安装Pipenv， 若失败，请手动安装python3.10
pip install pipenv
ECHO Install ENV
ECHO 正在安装环境
pipenv install
echo Install end
ECHO 安装结束，如为见报错则安装成功
pause