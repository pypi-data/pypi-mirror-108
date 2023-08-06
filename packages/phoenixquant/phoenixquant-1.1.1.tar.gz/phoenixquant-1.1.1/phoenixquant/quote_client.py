# -*- coding=utf-8 -*-

import zmq
import json
import os
import shelve
from itertools import product
from tempfile import gettempdir
from queue import Queue
from threading import Thread

json_name = [
    "amount",
    "ask_price_1",
    "ask_price_2",
    "ask_price_3",
    "ask_price_4",
    "ask_price_5",
    "ask_volume_1",
    "ask_volume_2",
    "ask_volume_3",
    "ask_volume_4",
    "ask_volume_5",
    "average",
    "bid_price_1",
    "bid_price_2",
    "bid_price_3",
    "bid_price_4",
    "bid_price_5",
    "bid_volume_1",
    "bid_volume_2",
    "bid_volume_3",
    "bid_volume_4",
    "bid_volume_5",
    "close",
    "datetime",
    "exchange",
    "highest",
    "last_price",
    "lower_limit",
    "lowest",
    "name",
    "open",
    "open_interest",
    "symbol",
    "upper_limit",
    "volume",
]


class QuoteClient:
    recv_buffer = Queue()

    threads = []
    ip_addr = [
        "tcp://1.15.233.244",  # 上海服务器-主
        "tcp://1.15.232.235",  # 上海服务器-主
        "tcp://121.5.156.40",  # 上海服务器-备用
    ]
    port_map = {
        "stock": "2525",  # 股票
        "future": "2626",  # 期货
        "option": "2727",  # 股指期权
        "index": "2828",  # 中证指数
        "future_index": "2929",  # 期货指数
    }

    def __init__(self, callback):
        self.callback = callback

    def reciver(self, address):
        context = zmq.Context(1)
        socket = context.socket(zmq.SUB)
        socket.connect(address)
        socket.setsockopt_string(zmq.SUBSCRIBE, "")  # 消息过滤
        socket.setsockopt(zmq.TCP_KEEPALIVE, 1)
        socket.setsockopt(zmq.TCP_KEEPALIVE_IDLE, 120)
        socket.setsockopt(zmq.TCP_KEEPALIVE_INTVL, 1)

        while True:
            response = socket.recv()
            result = json.loads(response)
            for item in result:
                tick = dict(zip(json_name, item))
                self.recv_buffer.put(tick)


    def process(self):
        cache_file = os.path.join(gettempdir(), "recv_quotes_cache")
        with shelve.open(cache_file, writeback=True) as cache_client:
            while True:
                tick = self.recv_buffer.get()
                key = tick["symbol"] + tick["exchange"]
                # 多线服务器，过滤重复行情
                if cache_client.get(key, None) == tick["datetime"]:
                    continue
                # print(tick["datetime"], tick["name"])
                self.callback(tick)
                cache_client[key] = tick["datetime"]


    def subscribe(self, marker):
        """
        支持：stock future option index future_index
        """
        if isinstance(marker, list):
            ports = [self.port_map[m] for m in marker]
        else:
            ports = [self.port_map[marker]]

        servers = [":".join(v) for v in product(self.ip_addr, ports)]
        for item in servers:
            self.threads.append(Thread(target=self.reciver, args=(item,)))
        self.threads.append(Thread(target=self.process))

        for t in self.threads:
            t.start()
        for t in self.threads:
            t.join()

if __name__ == "__main__":
    client = QuoteClient(print)
    client.subscribe("future")