FROM python:3.9-alpine
WORKDIR /root
COPY *.py requirements.txt /root/
RUN pip3 install -r requirements.txt
CMD [ "python3", "/root/main_client.py" ]