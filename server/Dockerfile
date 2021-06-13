FROM python:3.9
WORKDIR /root
COPY requirements.txt /root/
#RUN pip3 install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt
RUN pip3 install -r requirements.txt
COPY *.py /root/
CMD [ "python3", "/root/daemon_server.py" ]