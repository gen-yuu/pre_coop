FROM ubuntu:20.04
USER root

ENV WORK=/workdir
#rootで行う
USER root
WORKDIR ${WORK}

RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

RUN apt-get update
RUN apt install -y sudo git vim 

#pythonライブラリのインストール
RUN sudo apt install -y python3-pip
COPY requirements.txt .
RUN python3 -m pip install -U pip
#WSGI以外インストール
RUN pip3 install -r requirements.txt

#RabbitMQのインストール
RUN sudo apt-get install -y rabbitmq-server
RUN service rabbitmq-server start

#Apacheインストール
RUN sudo apt-get install -y apache2
#WSGIのインストール
RUN sudo apt install -y apache2-dev
RUN pip3 install mod-wsgi
#実行環境のリンクを張る
RUN sudo ln -sT /coop  /var/www/html/coop
#Apacheディレクティブの修正
COPY 000-default.conf ./etc/apache2/sites-enabled/

#モジュールの実行権限の付与
RUN sudo chmod 777 /usr/local/lib/python3.8/dist-packages/mod_wsgi/server/mod_wsgi-py38.cpython-38-x86_64-linux-gnu.so

COPY apache2.conf /etc/apache2/

RUN git clone https://github.com/Nshisei/coop.git

