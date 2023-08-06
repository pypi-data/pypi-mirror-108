from me_main_libs import *
from functools import lru_cache


def read_ts_inverted(ts_df):
    ts_df = ts_df*-1
    ts_df = ts_df+ts_df.min()*-1
    ts_df.columns = [x+'_inverted' for x in ts_df.columns]
    return ts_df


def read_ts_negative_zone(ts_df):
    ts_df = ts_df.copy()
    ts_df[ts_df > 0] = 0
    ts_df.columns = [x+'_negative_zone' for x in ts_df.columns]
    return ts_df


def read_ts_positive_zone(ts_df):
    ts_df = ts_df.copy()
    ts_df[ts_df < 0] = 0
    ts_df.columns = [x+'_positive_zone' for x in ts_df.columns]
    return ts_df


def read_ts_drawdown(ts_df):
    data = {}
    for x in ts_df.columns:
        data[x+'_drawdown'] = _read_ts_drawdown(ts_df[x])
    data = pd.concat(data, axis=1)
    return data


def read_ts_drawdown_rolling(ts_df, window):
    '''
    takes too much time
    '''
    data = pd.DataFrame()
    for x in ts_df.columns:
        col = x + f'_drawdown_roll_{window}'
        data[col] = _read_ts_rolling_drawdown(ts_df[x], window)
    return data


def _read_ts_drawdown(ts):
    if ts.min() < 0:
        ts = ts+abs(ts.min())
    ts = ts.dropna()
    running_max = np.maximum.accumulate(ts)
    running_max[running_max < 1] = 1
    return (ts)/running_max - 1


def _read_ts_rolling_drawdown(ts, window):
    data = ts.rolling(window, min_periods=window)
    data = [_read_ts_drawdown(
        x).tail(1) for x in data]
    data = pd.concat(data)
    return data


def read_ts_performance(ts_series, name):
    returns = ts_series.pct_change().dropna()
    returns.name = name+'_ret'

    cum_return = (1+returns).cumprod()
    cum_return.name = name+'_cret'

    drawdown = read_ts_drawdown(
        pd.DataFrame(cum_return)).squeeze()
    drawdown.name = name+'_dd'

    performance = {'cum_return': cum_return,
                   'drawdown': drawdown,
                   'returns': returns}
    return performance


def read_ts_performance_vs_spy(ts_series, name):
    ts1 = read_ts_performance(ts_series, name)
    spy = read_ts_performance(spy_adjClose(), 'spy')

    returns = pd.concat([ts1['returns'], spy['returns']],
                        axis=1).fillna(method='ffill').dropna()
    cum_returns = pd.concat([ts1['cum_return'], spy['cum_return']], axis=1).fillna(
        method='ffill').dropna()
    drawdowns = pd.concat([ts1['drawdown'], spy['drawdown']],
                          axis=1).fillna(method='ffill').dropna()

    performance = {'cum_returns': cum_returns,
                   'drawdowns': drawdowns,
                   'returns': returns}
    return performance


@lru_cache(maxsize=1)
def spy_adjClose():
    from yahoo_fin import stock_info
    data = stock_info.get_data('SPY')['adjclose']
    return data
