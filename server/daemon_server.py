import socket
import sys
import time
import asyncio
from datetime import datetime
from aiohttp import web
import config


async def send_heartbeat():
    global s, ip, port
    timestr = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    if ip == None or port == None:
        print(f"{timestr}-->{ip}:{port}")
    else:
        s.sendto(str.encode(timestr+"\n"), (ip, port))
        print(f"{timestr}-->{ip}:{port}")


async def handle(request):
    global s, ip, port
    ip = request.match_info['ip']
    port = int(request.match_info['port'])
    print(f"改变心跳地址{ip}:{port}")
    text = '{msg:"ok"}'
    return web.Response(text=text)

app = web.Application()
app.add_routes([web.get('/{ip}/{port}', handle)])


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

if __name__ == '__main__':
    global s, ip, port
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip = None
    port = None
    loop = asyncio.get_event_loop()
    cfg=config.ConfigManager()
    loop.create_task(run_heartbeat(cfg.read('heartbeat_interval')))
    run_httpserver(cfg.read('port'))
