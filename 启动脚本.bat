@ECHO off
ECHO ׼�������ű����������ʣ�����ϵhttps://github.com/JoeShu0/Image_Scrapper/issues��
ECHO  1��Pixiv
ECHO  2��GelBooru��NSFW��
ECHO  3��Pinterest
ECHO  4��Artstation
set /p Site=��ѡ����Ҫ��ȡ����վ��

IF %Site% == 1 (
    ECHO ��������Pixiv����ű�
    pipenv run python PixivScrap.py
) ELSE IF %Site% == 2 (
    ECHO ��������Gelbooru����ű�
    pipenv run python GelbooruScrap.py
) ELSE IF %Site% == 3 (
    ECHO ��������Pinterest����ű�
    pipenv run python PinterestScrap.py
) ELSE IF %Site% == 4 (
    ECHO ��������Artstation����ű�
    pipenv run python ArtstationScrap.py
) ELSE (
    ECHO ��Чѡ�񣬽ű������˳���
    pause
)
