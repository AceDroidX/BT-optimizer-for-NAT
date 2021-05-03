import requests
import pystun


def set_listen_port(api_port, bt_internal_port, api_ip="127.0.0.1") -> None:
    url = f"http://{api_ip}:{api_port}/api/v2/app/setPreferences?json=%7B%22listen_port%22:{bt_internal_port}%7D"
    response = requests.get(url)
    print(url)
    # if response.status!=200:
    print(response.status_code)
    print("qb的内部监听端口设置为"+str(bt_internal_port))


def get_listen_port(api_port, api_ip="127.0.0.1") -> int:
    url = f"http://{api_ip}:{api_port}/api/v2/app/preferences"
    response = requests.get(url)
    print(url)
    # if response.status!=200:
    print(response.status_code)
    print("qb的内部监听端口为"+str(response.json()["listen_port"]))
    return int(response.json()["listen_port"])


if __name__ == "__main__":
    print(get_listen_port())
    set_listen_port(55555)
