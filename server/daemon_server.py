import socket
import sys
import time
import asyncio
import traceback
from datetime import datetime
from aiohttp import web
import config


class ClientModel():
    def __init__(self, ip, port, name="default") -> None:
        self.ip = ip
        self.port = port
        self.name = name
        self.lastRequestTime = datetime.now().timestamp()


class ClientManager():
    def __init__(self) -> None:
        self.list = []

    def add(self, ip, port, name="default"):
        for client in self.list:
            if client.name == name:
                print(f"修改心跳地址[{name}]{ip}:{port}")
                client.ip = ip
                client.port = port
                client.lastRequestTime = datetime.now().timestamp()
                return
        print(f"添加心跳地址[{name}]{ip}:{port}")
        client = ClientModel(ip, port, name)
        self.list.append(client)

    def remove(self, client):
        print(f'已删除[{client.name}]{client.ip}:{client.port}')
        self.list.remove(client)

    def getList(self):
        return self.list


async def send_heartbeat():
    global s, clientManager
    timestr = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    if len(clientManager.getList()) == 0:
        print(f'{timestr}--No Client')
    for client in clientManager.getList():
        if client.ip != None and client.port != None:
            s.sendto(str.encode(timestr+"\n"), (client.ip, client.port))
        print(f"{timestr}-->[{client.name}]{client.ip}:{client.port}")


async def handle(request):
    global clientManager
    try:
        ip = request.match_info['ip']
        port = int(request.match_info['port'])
        try:
            name = request.match_info['name']
        except KeyError:
            name = "default"
        print(f"新心跳地址请求[{name}]{ip}:{port}")
        clientManager.add(ip, port, name)
        return web.Response(status=200, text='{msg:"ok"}')
    except Exception as e:
        traceback.print_exc()
        return web.Response(status=403, text='{msg:"err"}')

app = web.Application()
app.add_routes([web.get('/{ip}/{port}', handle),
               web.get('/{ip}/{port}/{name}', handle)])


def run_httpserver(port):
    web.run_app(app, port=port)


async def run_heartbeat(interval):
    try:
        while True:
            await send_heartbeat()
            await asyncio.sleep(interval)
    except KeyboardInterrupt:
        print("close")
        s.close()


async def clean_client(timeout, interval=1):
    global clientManager
    try:
        while True:
            for client in clientManager.getList():
                if datetime.now().timestamp()-client.lastRequestTime > timeout:
                    clientManager.remove(client)
            await asyncio.sleep(interval)
    except KeyboardInterrupt:
        print("close")
        s.close()

if __name__ == '__main__':
    global clientManager
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clientManager = ClientManager()
    loop = asyncio.get_event_loop()
    cfg = config.ConfigManager()
    loop.create_task(clean_client(cfg.read('client_request_timeout')))
    loop.create_task(run_heartbeat(cfg.read('heartbeat_interval')))
    run_httpserver(cfg.read('port'))
