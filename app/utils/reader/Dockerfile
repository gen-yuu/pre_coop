FROM ubuntu:20.04
USER root

#タイムゾーンの設定
RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

RUN apt-get update
RUN apt install -y sudo vim 

#USBデバイスを扱うプログラムをOSを意識せずに扱えるライブラリをインストール
RUN sudo apt-get update
RUN sudo apt install -y libusb-dev python3-usb

#pythonライブラリのインストール
RUN sudo apt install -y python3-pip
COPY requirements.txt .
RUN python3 -m pip install -U pip
RUN pip3 install -r requirements.txt

#実行ファイル
COPY ./app/utils/sqls /usr/coop/sqls
COPY ./app/utils/reader/nfc_read.py /usr/coop/nfc_read.py
COPY ./app/utils/connect_db.py /usr/coop/connect_db.py