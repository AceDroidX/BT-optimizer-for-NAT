import mitmproxy.http
from mitmproxy import ctx
import binascii
from datetime import datetime


class ModifyQuery:
    def __init__(self, external_port):
        self.external_port = external_port
        print(f"设置mitm外部端口为{external_port}")

    def request(self, flow: mitmproxy.http.HTTPFlow):
        if "info_hash" in flow.request.query:
            timestr = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            print(f"[{timestr}]{flow.request.pretty_host}-----{flow.request.query['port']}")
            # print(f"{flow.request.pretty_host}-----{flow.request.query['port']}")
            flow.request.query["port"] = str(self.external_port)
        # flow.request.query["mitmproxy"] = "rocks"


# addons = [
#     ModifyQuery(50000)
# ]
