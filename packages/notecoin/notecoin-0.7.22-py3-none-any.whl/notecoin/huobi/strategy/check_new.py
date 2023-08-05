import json
from time import sleep

from notecoin.huobi.client import GenericClient
from notecoin.huobi.strategy.message import HuoBiMessage
from notecoin.huobi.strategy.trade_order import TradeOrder
from notetool.time import WorkTime, now2unix
from notetool.tool.log import logger
from notetool.tool.secret import read_secret


class FindNewCoin:
    def __init__(self):
        self.unix = 0
        self.msg_huobi = HuoBiMessage()
        self.work_time = WorkTime()

        api_key = read_secret(cate1='coin', cate2='huobi', cate3='api_key')
        secret_key = read_secret(cate1='coin', cate2='huobi', cate3='secret_key')

        self.generic = GenericClient(api_key=api_key, secret_key=secret_key)
        self.symbol_df_last = None
        self.symbol_df_now = None
        self.symbol_dict = {}

    def init(self):
        df = self.generic.get_exchange_symbols().data
        self.symbol_df_last = self.symbol_df_now = df
        symbols = df[['symbol', 'state']].values
        for symbol, status in symbols:
            self.symbol_dict[symbol] = status

    def update(self, df):
        self.symbol_df_last = self.symbol_df_now
        self.symbol_df_now = df

        for _symbol in json.loads(df.to_json(orient="records")):
            symbol, state = _symbol['symbol'], _symbol['state']

            if symbol not in self.symbol_dict.keys():
                self.msg_huobi.send_msg(f"new symbol:{symbol}:{state}")
                self.symbol_dict[symbol] = state
                self.new_coin(_symbol)

            elif state != self.symbol_dict[symbol]:
                self.msg_huobi.send_msg(f"state change:{symbol}:{self.symbol_dict[symbol]}->{state}")
                self.symbol_dict[symbol] = state
                self.new_coin(_symbol)
            else:
                pass

    def new_coin(self, _symbol):
        symbol, state = _symbol['symbol'], _symbol['state']
        if state == 'online' and _symbol['quote-currency'] == 'usdt' and not symbol.endswith("3lusdt"):
            trade = TradeOrder()
            trade.buy(symbol=_symbol['symbol'], amount=50 * _symbol['min-order-value'])
            self.msg_huobi.send_msg(f"buy new coin:{symbol}:{self.symbol_dict[symbol]}->{state}")

    def run(self):
        self.init()
        while True:
            try:
                df = self.generic.get_exchange_symbols().data
                self.update(df)
                unix = now2unix()
                if unix - self.unix > 86400:
                    self.info()
                    self.unix = unix

                if self.work_time.time_to_day_end(unix):
                    sleep(0.1)
                elif self.work_time.time_to_hour_end(unix):
                    sleep(0.1)
                elif self.work_time.time_to_ten_minute_end(unix):
                    sleep(0.5)
            except Exception as e:
                print(e)
                logger.info(f"error:{e}")

    def info(self):
        status_dict = {}
        for k, v in self.symbol_dict.items():
            ks = status_dict.get(v, [])
            ks.append(k)
            status_dict[v] = ks

        for k, v in status_dict.items():
            self.msg_huobi.send_msg(f"{k}:\t{', '.join(v)}")
            pass


find = FindNewCoin()
find.run()

# ps -elf|grep check_new
# nohup /root/anaconda3/bin/python3.8 /root/workspace/notechats/notecoin/notecoin/huobi/strategy/check_new.py >>/root/workspace/tmp/notecoin-check-run-$(date +%Y-%m-%d).log 2>&1 &
