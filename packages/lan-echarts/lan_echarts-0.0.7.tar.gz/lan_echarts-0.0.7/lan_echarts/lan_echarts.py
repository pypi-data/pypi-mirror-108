import asyncio
import json
import os
import threading
import time
from typing import Optional, Awaitable, Tuple, Dict, List
import requests

import tornado.ioloop
import tornado.web
import tornado.websocket

_Ech = {}


# noinspection PyProtectedMember
def create_echarts(server_port, name="noname"):
    if server_port in _Ech:
        return _Ech[server_port]
    else:
        e = LanEcharts(server_port, name)
        _Ech[server_port] = e
        e._start()
        while e._started is False:
            pass
        return e


class LanEcharts:
    def __init__(self, server_port, name="noname") -> None:
        self.server_port = server_port
        self.view_name = name

    def view_ready_len(self):
        return len(self._view_page_ws)

    def render(self, charts: List[Tuple[Tuple[int, int], Dict]]):
        res = requests.post("http://127.0.0.1:" + str(self.server_port), json=charts).json()
        if res["status"] == "200":
            return [True, res["message"]]
        else:
            return [False, res["message"]]

    _started = False

    def _check_started(self):
        if self._started:
            print("start LanEcharts: http://127.0.0.1:{}".format(self.server_port))
        return self._started

    def _start(self):
        if self._check_started():
            return self

        def t():
            asyncio.set_event_loop(asyncio.new_event_loop())
            app = tornado.web.Application(handlers=[
                (r"/", self._v_handler()),
                (r"/ws", self._ws_handler())
            ], debug=False, **self._settings)
            print(self._settings)
            app.listen(self.server_port)
            print("start LanEcharts: http://127.0.0.1:{}".format(self.server_port))
            self._started = True
            tornado.ioloop.IOLoop.current().start()

        threading.Thread(target=t, args=()).start()
        return self

    _settings = {
        'template_path': os.path.join(os.path.dirname(__file__), "static"),
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        # "static_url_prefix": "statics/",
    }
    _view_page_ws = []

    def _v_handler(self):
        _that = self

        class _DHandler(tornado.web.RequestHandler):

            def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
                pass

            # 添加一个处理get请求方式的方法

            def get(self):
                self.render('echarts.html', server_port=_that.server_port, view_name=_that.view_name)

            def post(self):
                post_data = self.request.body.decode('utf-8')
                for v in _that._view_page_ws:
                    v.write_message(post_data)
                self.write(json.dumps({
                    "status": "200",
                    "message": "LanEcharts sent to {} - {}".format(len(_that._view_page_ws), str(time.time()))
                }))

        return _DHandler

    def _ws_handler(self):
        _that = self

        class _WsHandler(tornado.websocket.WebSocketHandler):

            def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
                pass

            def open(self, *args, **kwargs):
                _that._view_page_ws.append(self)
                print("LanEcharts accept: {}".format(_that.view_ready_len()))

            def on_message(self, message):
                if message.startswith("hello_open"):
                    self.write_message("hello_open_" + _that.view_name)
                else:
                    self.write_message(message)

            # 关闭连接时被调用
            def on_close(self):
                if self in _that._view_page_ws:
                    _that._view_page_ws.remove(self)
                print("LanEcharts closed: {}".format(_that.view_ready_len()))

        return _WsHandler


if __name__ == "__main__":
    LanEcharts(name="a", server_port=9988)._start()
    print(111)

"""

"""
