import datetime
import pandas as pd
import numpy as np
from finlab.report import Report
from . import data

def sim(buy, sell=None, resample=None, weight=None, trade_at_price='close', benchmark=None, fee_ratio=1.425/1000, tax_ratio=3/1000, name=None, code_upload=False):

    # adjust for trading price
    if trade_at_price == 'open':
        price = data.get('etl:adj_open')
    elif trade_at_price == 'close':
        price = data.get('etl:adj_close')
    else:
        price = (data.get('etl:adj_close') + data.get('etl:adj_open'))/2
        
    # resample dates
    if isinstance(resample, str):
        dates = pd.date_range(buy.index[0], buy.index[-1], freq=resample)
        next_trading_date = min(set(pd.date_range(buy.index[0], 
            datetime.datetime.now() + datetime.timedelta(days=720),
            freq=resample)) - set(dates))
    elif resample is None:
        dates = None

    # calculate position using buy and sell
    positions = calculate_position(price, buy, sell, dates, weight)
    returns = calculate_capital(price, positions, fee_ratio, tax_ratio)

    # create report
    r = Report(returns, positions, benchmark, fee_ratio, tax_ratio, trade_at_price, next_trading_date)

    try:
        obj = r.upload(name, code=code_upload)
        url = 'https://finlab-python.github.io/strategy/?uid=' + obj['uid'] + '&sid=' + obj['strategy_id']
        from IPython.display import IFrame, display
        iframe = IFrame(url, width='100%', height=800)
        display(iframe)
        
    except Exception as e:
        print('Catch error during render iframe')
        print(str(e))

    return r

def rebalance_dates(freq):
    if isinstance(freq, str):
        def f(start_date, end_date):
            return pd.date_range(start_date, end_date, freq=freq)
        return f
    elif isinstance(freq, pd.Series):
        def f(start_date, end_date):
            return pd.to_datetime(freq.loc[start_date, end_date].index)
    return f

def adjust_dates_to_index(creturn, dates):

    def to_buesiness_day(d):
        if d <= creturn.index[-1]:
            i = creturn.index.get_loc(d, method='bfill')
            ret = creturn.index[i]
        else:
            ret = None#creturn.index[-1]
        return ret

    return pd.DatetimeIndex(pd.Series(dates).apply(to_buesiness_day).dropna()).drop_duplicates()

def calculate_position(price, buy, sell, resample=None, weight=None):

    '''
    signalIn and signalOut are pandas dataframe, which indicate a stock should be
    bought or not.
    '''

    if sell is not None:
        buy &= price.notna()
        sell |= price.isna()

    position = pd.DataFrame(np.nan, index=buy.index, columns=buy.columns)

    position[buy.fillna(False)] = 1
    if sell is not None:
        position[sell.fillna(False)] = 0
        position = position.ffill()
    position = position.fillna(0)

    if weight is not None:
      position *= weight.reindex_like(position).fillna(0)

    position = position.div(position.abs().sum(axis=1), axis=0).fillna(0)

    if resample is not None:
        dates = adjust_dates_to_index(price, resample)
        # position = position.reindex(price.index, method='ffill')\
        #     .reindex(dates, method='ffill')\
        #     .reindex(price.index, method='ffill').astype(float)
        position = position.reindex(dates, method='ffill').astype(float)

    # remove stock not traded
    position = position.loc[:, position.sum()!=0]

    # remove zero portfolio time period
    position = position.loc[(position.sum(axis=1) != 0).cumsum() != 0]
    return position

def calculate_capital(price, position, fee_ratio, tax_ratio):

    # shapes of price and position should be the same
    # value of price and position should not be Nan
    adj_close = price.loc[position.index[0]:][position.columns.intersection(price.columns)]
    position = position.reindex(price.index, method='ffill').ffill().fillna(0)

    # forbid trading at the stock listing date
    position[adj_close.ffill().shift().isna() & adj_close.notna()] = 0

    # calculate position adjust dates
    periods = (position.diff().abs().sum(axis=1) > 0).cumsum()
    indexes = pd.Series(periods.index).groupby(periods.values).last()

    # calculate periodic returns
    selected_adj = (adj_close.shift(-2)/adj_close.shift(-1)).clip(0.9 ,1.1).groupby(periods).cumprod().fillna(1)
    selected_adj[((position == 0) | (selected_adj == 0))] = np.nan
    ret = (selected_adj.fillna(1) * position).sum(axis=1) + (1 - position.sum(axis=1))

    # calculate cost
    pdiff = position.diff()
    pdiff[pdiff > 0] *= (fee_ratio)
    pdiff[pdiff < 0] *= (fee_ratio + tax_ratio)
    cost = pdiff.abs().sum(axis=1).shift()
    cost = cost.fillna(0)

    # calculate cummulation returns
    s = (pd.Series(ret.groupby(periods).last().values, indexes).reindex(ret.index).fillna(1).shift().cumprod() * ret)

    # consider cost
    cap = ((s.shift(-1) / s).shift(3) * (1-cost)).cumprod().fillna(1)

    return cap[cap.shift(-1).fillna(1) != 1.0]