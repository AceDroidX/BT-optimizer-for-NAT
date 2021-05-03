import requests


def set_remote_heartbeat(external_ip: str, external_port: int, remote_url: str):
    url = f"{remote_url}/{external_ip}/{external_port}"
    r = requests.get(url)
    print(f"设置远程心跳{url}")
    if r.status_code == 200:
        return True
    else:
        print(f'设置失败:{r.status_code}')
        return False


if __name__ == '__main__':
    set_remote_heartbeat("test.ip", 42711, "https://aaa.bbb")