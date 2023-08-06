import os
import json
import pandas as pd
from time import sleep
from urllib import parse, request
from datetime import datetime
from functools import partial


class DataClient:
    """
    支持类型：
    期货合约：SHFE.rb2110
    现货合约：SSWE.ALH
    期权合约：CFFEX.IO2003-C-3900，CZCE.TA004P4550
    交易所组合：CZCE.SPD AP709&CF801，CZCE.IPS SF709&SM709，DCE.SP pp1709&pp1805
    主力合约：SHFE.rb@MAIN，指数合约：SHFE.rb@INDEX
    中证指数：CSI.000300
    深圳股票：SZSE.000001，上海股票：SSE.600000
    指数：SSE.000016 上证50指数，SSE.000300 沪深300指数 SSE.000905 中证500指数
    ETF：SSE.510050 上交所上证50etf SSE.510300 上交所沪深300etf SZSE.159919 深交所沪深300etf
    ETF期权：SSE.10002513，SSE.10002504，SZSE.90000097
    """

    base_url = "https://service-an8w6tgn-1253762454.sh.apigw.tencentcs.com"

    def __init__(self, token="", debug=False):
        self.debug = debug
        self.token = os.environ["DC_TOKEN"] if "DC_TOKEN" in os.environ else token

        self.get_bars = partial(self.history, data_type="bar", freq="QS")
        self.get_ticks = partial(self.history, data_type="tick", freq="12BH")
        self.get_dailys = partial(self.history, data_type="daily", freq="YS")

    def status_check(self):
        while True:
            try:
                with request.urlopen(self.base_url + "/status") as response:
                    json_data = json.loads(response.read())
                    if json_data.get("status", None) == "ok":
                        break
                    else:
                        raise "database is pending..."
            except Exception as e:
                print(e)
                sleep(1)

    def history(self, symbol, start_data, end_date, data_type, freq):
        date_split = pd.date_range(start_data, end_date, freq=freq)
        date_split = [start_data, *date_split, end_date]
        data = pd.DataFrame()
        self.status_check()
        for index, _ in enumerate(date_split):
            if index + 1 != len(date_split):
                args = {
                    "token": self.token,
                    "symbol": symbol,
                    "data_type": data_type,
                    "start_date": datetime.strftime(date_split[index], "%Y%m%d%H%M%S"),
                    "end_date": datetime.strftime(date_split[index+1], "%Y%m%d%H%M%S"),
                }
                try:
                    df = pd.read_json(
                        self.base_url + "/md?" + parse.urlencode(args), orient="split"
                    ).set_index("datetime")
                    data = data.append(df)
                    if self.debug:
                        print("下载完成", date_split[index], "~", date_split[index+1])
                except:
                    pass

        return data.drop_duplicates()


if __name__ == "__main__":
    client = DataClient("your token!")
    # 日线
    dailys = client.get_dailys(
        "CFFEX.IF@INDEX",
        start_data=datetime(2018, 1, 1),
        end_date=datetime(2021, 6, 4)
    )
    print(dailys)
    # 分钟
    bars = client.get_bars(
        "SHFE.rb@INDEX",
        start_data=datetime(2021, 5, 6, 21, 0, 0),
        end_date=datetime(2021, 6, 4, 15, 0, 0)
    )
    print(bars)

    # tick
    ticks = client.get_ticks(
        "SHFE.rb2110",
        start_data=datetime(2021, 6, 3, 21, 0, 0),
        end_date=datetime(2021, 6, 4, 15, 0, 0)
    )
    print(ticks)
