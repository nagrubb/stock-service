#!/usr/bin/env python3
import sys
import os
import signal
from functools import wraps
from flask import Flask, jsonify
from alpha_vantage.timeseries import TimeSeries
from waitress import serve
from stock_service.config import Config
from redis import Redis

ts = None
init_error = None
application = Flask(__name__)
GlobalConfig = Config(os.environ)

SECONDS_IN_A_MINUTES = 60

try:
    GlobalConfig.print()
    ts = TimeSeries(GlobalConfig.alpha_vantage_api_key)
    if ts is None:
        raise RuntimeError('Failed to create TimeSeries object')
except Exception as e:
    init_error = str(e)


def sigtermHandler(signalNumber, frame):
    print('Exiting from SIGTERM')
    sys.exit(1)


@application.route("/api/v1/stock/<symbol>")
def stock(symbol: str) -> str:
    try:
        if init_error:
            return jsonify(error=init_error), 500

        symbol = symbol.upper()
        closing_price = Redis(host=GlobalConfig.redis_server,
                              port=GlobalConfig.redis_port).get(symbol)

        if not closing_price:
            print(
                "Api=GetStock Action=UsingAlphaVantage Symbol={0}".format(symbol))
            data, meta_data = ts.get_intraday(symbol)
            last_refresh = meta_data['3. Last Refreshed']
            last_data = data[last_refresh]
            closing_price = last_data['4. close']
            Redis(host=GlobalConfig.redis_server, port=GlobalConfig.redis_port).set(
                symbol, closing_price, ex=GlobalConfig.cache_duration_in_minutes * 60)
        else:
            closing_price = closing_price.decode("utf-8")
            print(
                "Api=GetStock Action=UsingRedisCache Symbol={0}".format(symbol))

        return jsonify(
            symbol=symbol,
            closing_price=closing_price
        )
    except Exception as e:
        print(e)
        return jsonify(error=str(e)), 500


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, sigtermHandler)
    serve(application, host='0.0.0.0', port=80)
