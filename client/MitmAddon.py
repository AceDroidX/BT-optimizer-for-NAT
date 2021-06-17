import mitmproxy.http
from mitmproxy import ctx
import binascii
from datetime import datetime
import logging


class ModifyQuery:
    def __init__(self, external_port, http_rewrite):
        self.external_port = external_port
        self.http_rewrite = http_rewrite
        logging.info(f"设置mitm外部端口为{external_port}")
        if http_rewrite != "":
            logging.info(f"设置http重写的域名为{http_rewrite}")

    def request(self, flow: mitmproxy.http.HTTPFlow):
        if "info_hash" in flow.request.query:
            timestr = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            logging.info(
                f"[{timestr}]{flow.request.pretty_host}-----{flow.request.query['port']}")
            # logging.info(f"{flow.request.pretty_host}-----{flow.request.query['port']}")
            flow.request.query["port"] = str(self.external_port)
        if flow.request.pretty_host == self.http_rewrite and flow.request.scheme == "http":
            logging.info(f"[{timestr}]{flow.request.pretty_host}-----http")
            flow.request.scheme = "https"
        # flow.request.query["mitmproxy"] = "rocks"


# addons = [
#     ModifyQuery(50000)
# ]
