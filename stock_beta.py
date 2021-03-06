import logging

import pandas as pd
from tigeropen.common.consts import BarPeriod

from lib.date import date_delta, get_today
from lib.quant import alpha_beta
from tiger.config import get_bars_from_cache, get_quote_client

"""
波动率计算
https://blog.csdn.net/CoderPai/article/details/82868280

beta 计算
https://blog.csdn.net/thfyshz/article/details/83443783

贝塔系数衡量了个股或基金相对于整个股市的波动情况。
β范围	含义
β=1	    股票或基金的风险收益率与市场平均风险收益率相同
β>1	    股票或基金的风险相较于市场平均更大
β<1	    股票或基金的风险相较于市场平均更小
"""

logging.basicConfig(format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', level=logging.INFO)


def alpha_beta_plot(data: pd.DataFrame, stocks: []):
    """
    Alpha, Beta 展示
    :param data: 数据
    :param stocks: 股票
    :return:
    """
    spy_data = data.loc[(data["symbol"] == 'SPY')]
    qqq_data = data.loc[(data["symbol"] == 'QQQ')]

    return_qqq = list(qqq_data['close'].pct_change().dropna())
    return_spy = list(spy_data['close'].pct_change().dropna())

    for stock in stocks:
        stock_data = data.loc[(data["symbol"] == stock)]

        return_stock = list(stock_data['close'].pct_change().dropna())

        # 以SPY为基准计算alpha, beta
        alpha_spy, beta_spy = alpha_beta(return_spy, return_stock)

        alpha_qqq, beta_qqq = alpha_beta(return_qqq, return_stock)

        logging.info('SPY basics %s alpha: %s, beta: %s', stock, str(alpha_spy), str(beta_spy))

        logging.info('QQQ basics %s alpha: %s, beta: %s', stock, str(alpha_qqq), str(beta_qqq))


if __name__ == '__main__':
    quote_client = get_quote_client()

    stocks = ['QQQ', 'SPY', 'TLT', 'USO', 'IAU']

    data = get_bars_from_cache(quote_client, symbols=stocks, period=BarPeriod.DAY,
                               begin_time=date_delta(-52 * 8), end_time=get_today())

    alpha_beta_plot(data, stocks)

    

