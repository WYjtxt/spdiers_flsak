# FROM <基础镜像>
FROM python:3.8.16
WORKDIR /spiders
COPY requirements.txt ./
# 安装requirements.txt 中指定的任何所需软件包
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY . .
ENV LANG C.UTF-8

CMD ["gunicorn", "main:app","-c","./gunicorn.conf.py"]