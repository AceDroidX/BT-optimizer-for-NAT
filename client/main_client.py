import MitmAddon
import pystun
import qbtapi
import daemon_client
import time
import asyncio
import config


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


def nat_test(source_port):
    for i in range(5):
        nat_type, external_ip, external_port = pystun.get_ip_info(
            source_port=source_port, stun_host='stun.qq.com')
        if nat_type == pystun.FullCone:
            print(f"第{i}次测试成功:{nat_type, external_ip, external_port}")
            return True, nat_type, external_ip, external_port
        else:
            print(f"第{i}次测试失败:{nat_type, external_ip, external_port}")
            time.sleep(1)
    if i == 5:
        print("您的设备FullCone测试失败，请检查路由器设置")
        return False, nat_type, external_ip, external_port


def main():
    cfg = config.ConfigManager()
    internal_port = cfg.read("internal_port")
    print('检查设定的端口是否已被占用')
    if qbtapi.get_listen_port(cfg.read("api_port")) == internal_port:
        # todo random port number
        qbtapi.set_listen_port(cfg.read("api_port"), 15464)
    print('检查设定的端口在外部的映射')
    result, nat_type, external_ip, external_port = nat_test(internal_port)
    # 非Fullcone退出
    if not result:
        return
    port_map = [internal_port, external_port]
    # loop = asyncio.get_event_loop()
    # loop.run_in_executor(None, start_mitm,(external_port,))
    print("休眠一秒")
    time.sleep(1)
    print('改回设定好的端口')
    qbtapi.set_listen_port(cfg.read("api_port"), internal_port)
    if cfg.read("remote_enable"):
        print("设置远程心跳地址")
        daemon_client.set_remote_heartbeat(
            external_ip, external_port, cfg.read("remote_url"))
    print('修改Tracker里的port信息')
    start_mitm(cfg.read("proxy_port"), external_port)


if __name__ == "__main__":
    main()