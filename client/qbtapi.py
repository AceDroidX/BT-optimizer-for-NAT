import requests
import pystun
import logging


def set_listen_port(api_port, api_host, bt_internal_port) -> None:
    url = f"http://{api_host}:{api_port}/api/v2/app/setPreferences?json=%7B%22listen_port%22:{bt_internal_port}%7D"
    response = requests.get(url)
    logging.info(url)
    # if response.status!=200:
    logging.info(response.status_code)
    logging.info("qb的内部监听端口设置为"+str(bt_internal_port))


def get_listen_port(api_port, api_host) -> int:
    url = f"http://{api_host}:{api_port}/api/v2/app/preferences"
    response = requests.get(url)
    logging.info(url)
    # if response.status!=200:
    logging.info(response.status_code)
    logging.info("qb的内部监听端口为"+str(response.json()["listen_port"]))
    return int(response.json()["listen_port"])


if __name__ == "__main__":
    logging.info(get_listen_port())
    set_listen_port(55555)
