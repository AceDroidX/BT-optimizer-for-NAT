import MitmAddon
import pystun
import qbtapi
import daemon_client
import time
import threading
import asyncio
import traceback
import config
import logging


def start_mitm(proxy_port, external_port):
    # https://github.com/sunfkny/genshin-gacha-export/blob/main/main.py
    from mitmproxy.options import Options
    from mitmproxy.proxy.config import ProxyConfig
    from mitmproxy.proxy.server import ProxyServer
    from mitmproxy.tools.dump import DumpMaster
    options = Options(listen_host="0.0.0.0",
                      listen_port=proxy_port, http2=True)
    config = ProxyConfig(options)
    global m
    m = DumpMaster(options, with_termlog=False, with_dumper=False)
    m.server = ProxyServer(config)
    m.addons.add(MitmAddon.ModifyQuery(external_port))
    m.run()


def stop_mitm():
    global m
    m.shutdown()
    logging.info("mitm已停止")


def nat_test(source_port):
    for i in range(5):
        try:
            nat_type, external_ip, external_port = pystun.get_ip_info(
                source_port=source_port, stun_host='stun.qq.com')
        except Exception as e:
            traceback.print_exc()
            nat_type = "Error"
            external_ip, external_port = (None, None)
        if nat_type == pystun.FullCone:
            logging.info(f"第{i}次测试成功:{nat_type, external_ip, external_port}")
            return True, nat_type, external_ip, external_port
        else:
            logging.info(f"第{i}次测试失败:{nat_type, external_ip, external_port}")
            time.sleep(1)
    if i == 5:
        logging.info("您的设备FullCone测试失败，请检查路由器设置")
        return False, nat_type, external_ip, external_port


def run_once(cfg):
    new_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)
    internal_port = cfg.read("internal_port")
    logging.info('检查设定的端口是否已被占用')
    if qbtapi.get_listen_port(cfg.read("api_port"), cfg.read("api_host")) == internal_port:
        # todo random port number
        qbtapi.set_listen_port(cfg.read("api_port"),
                               cfg.read("api_host"), 15464)
    logging.info('检查设定的端口在外部的映射')
    result, nat_type, external_ip, external_port = nat_test(internal_port)
    # 非Fullcone退出
    if not result:
        return
    port_map = [internal_port, external_port]
    logging.info("休眠一秒")
    time.sleep(1)
    logging.info('改回设定好的端口')
    qbtapi.set_listen_port(cfg.read("api_port"),
                           cfg.read("api_host"), internal_port)
    if cfg.read("remote_enable"):
        logging.info("设置远程心跳地址")
        global external
        external = [external_ip, external_port]
        daemon_client.set_remote_heartbeat(
            external_ip, external_port, cfg.read('remote_name'), cfg.read("remote_url"))
    logging.info('修改Tracker里的port信息')
    start_mitm(cfg.read("proxy_port"), external_port)
    # loop = asyncio.get_event_loop()
    # loop.run_in_executor(
    #     None, start_mitm, (cfg.read("proxy_port"), external_port,))


def main():
    cfg = config.ConfigManager()
    while True:
        t = threading.Thread(target=run_once, args=(cfg,))
        t.start()
        for _ in range(5):
            time.sleep(60)
            if cfg.read("remote_enable"):
                global external
                logging.info(f"设置远程心跳地址{external[0]}:{external[1]}")
                daemon_client.set_remote_heartbeat(
                    external[0], external[1], cfg.read('remote_name'), cfg.read("remote_url"))
        # time.sleep(60)
        stop_mitm()


if __name__ == "__main__":
    main()
