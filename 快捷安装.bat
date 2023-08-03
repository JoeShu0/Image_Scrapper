@ECHO off
ECHO 此脚本依赖于Python 3.10，若未安装，请在Requirement文件夹中找到安装程序并安装
pause
ECHO Installing Pipenv, If fails, please install python 3.10
ECHO 正在安装Pipenv， 若失败，请手动安装python3.10
pip install pipenv
ECHO Install ENV
ECHO 正在安装环境
pipenv install
echo Install end
<<<<<<< Updated upstream
ECHO 安装结束，如为见报错则安装成功
=======
ECHO 安装结束，如为未 报错 则安装成功
>>>>>>> Stashed changes
pause