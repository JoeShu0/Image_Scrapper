@ECHO off
ECHO 准备启动脚本，如有疑问，请联系https://github.com/JoeShu0/Image_Scrapper/issues：
ECHO  1，Pixiv
ECHO  2，GelBooru（NSFW）
ECHO  3，Pinterest
ECHO  4，Artstation
set /p Site=请选择需要爬取的网站：

IF %Site% == 1 (
    ECHO 正在启动Pixiv爬虫脚本
    pipenv run python PixivScrap.py
) ELSE IF %Site% == 2 (
    ECHO 正在启动Gelbooru爬虫脚本
    pipenv run python GelbooruScrap.py
) ELSE IF %Site% == 3 (
    ECHO 正在启动Pinterest爬虫脚本
    pipenv run python PinterestScrap.py
) ELSE IF %Site% == 4 (
    ECHO 正在启动Artstation爬虫脚本
    pipenv run python ArtstationScrap.py
) ELSE (
    ECHO 无效选择，脚本即将退出。
    pause
)
