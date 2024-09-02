import numpy as np
import pandas as pd
import sys
import json

CFG_MUTABLE = 'cfg_mutable.json'
CFG_IMMUTABLE = 'cfg_immutable.json'

def my_print(*args):
    print(pd.Timestamp('now'), end = ' ')
    print(*args)
    sys.stdout.flush()

def get_cfg(cfg_name):
    with open(cfg_name) as ifl:
        return json.load(ifl)

def get_gmv():
    return get_cfg(CFG_MUTABLE)['gmv']

def get_trade_cutoff():
    return get_gmv() / 7000

def get_barrier():
    return get_gmv() / 600

def get_prod():
    return get_cfg(CFG_IMMUTABLE)['prod']

def regularize_trades(t, run_barrier=True):
    prod = get_prod()
    if prod:
        assert isinstance(t, pd.Series)
        t = t.sort_index()
        index = list(t.index)
        t = t.values
    assert isinstance(t, np.ndarray)
    b = get_barrier()
    if run_barrier:
        t = np.where(np.abs(t) > b, t - np.sign(t) * b, 0.)
    else:
        my_print('IGNORING BARRIER')
    cut = get_trade_cutoff()
    my_print('b cut', b, cut)
    t = np.where(np.abs(t) > cut, t, 0.)
    if prod:
        t = pd.Series(t, index=index)
    return t

class ReconnectException(Exception):
    pass

def get_universe():
    fname = 'universe.json'
    with open(fname) as ifl:
        return eval(ifl.readline())