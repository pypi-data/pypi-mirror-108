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

Ech = {}


def create_echarts(server_port, name="noname"):
    if server_port in Ech:
        return Ech[server_port]
    else:
        e = Echarts(server_port, name)
        Ech[server_port] = e
        e.start()
        while e.started is False:
            pass
        return e


class Echarts:
    def __init__(self, server_port, name="noname") -> None:
        self.server_port = server_port
        self.view_name = name

    def render(self, charts: List[Tuple[Tuple[int, int], Dict]]):
        res = requests.post("http://127.0.0.1:" + str(self.server_port), json=charts).json()
        if res["status"] == "200":
            return [True, res["message"]]
        else:
            return [False, res["message"]]

    started = False

    def _check_started(self):
        if self.started:
            print("start echarts view at {}, http://127.0.0.1:{}".format(self.server_port, self.server_port))
        return self.started

    def start(self):
        if self._check_started():
            return

        def t():
            asyncio.set_event_loop(asyncio.new_event_loop())
            self.start_block()

        threading.Thread(target=t, args=()).start()
        return self

    def start_block(self):
        if self._check_started():
            return

        app = tornado.web.Application(handlers=[
            (r"/", self._v_handler()),
            (r"/ws", self._ws_handler())
        ], debug=True, **self._settings)
        print(self._settings)
        app.listen(self.server_port)
        print("start echarts view at {}, http://127.0.0.1:{}".format(self.server_port, self.server_port))
        self.started = True
        tornado.ioloop.IOLoop.current().start()

    """









    """
    _settings = {
        # 'template_path': 'echarts',
        "static_path": os.path.join(os.path.dirname(__file__)),
        # "static_url_prefix": "echarts/",
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
                for v in Echarts._view_page_ws:
                    v.write_message(post_data)
                self.write(json.dumps({
                    "status": "200",
                    "message": "sent {} view - {}".format(len(_that._view_page_ws), str(time.time()))
                }))

        return _DHandler

    def _ws_handler(self):
        _that = self

        class _WsHandler(tornado.websocket.WebSocketHandler):

            def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
                pass

            def open(self, *args, **kwargs):
                _that._view_page_ws.append(self)
                print("view accept size:{}".format(len(_that._view_page_ws)))

            def on_message(self, message):
                if message.startswith("hello_open"):
                    self.write_message("hello_open_" + _that.view_name)
                else:
                    self.write_message(message)

            # 关闭连接时被调用
            def on_close(self):
                if self in _that._view_page_ws:
                    _that._view_page_ws.remove(self)
                print("view closed size={}".format(len(_that._view_page_ws)))

        return _WsHandler


if __name__ == "__main__":
    Echarts(name="a", server_port=9988).start()
    print(111)

"""

"""
