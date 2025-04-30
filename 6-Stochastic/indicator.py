import numpy as np
import pandas as pd

def stochastic_dict(k_fast,d_slow,dd_slow,var):

    if 'k_fast' and 'd_slow' and 'dd_slow' not in var:
        for i in ['k_fast','d_slow','dd_slow']:
            var[i]=[]

    #fast:
    if len(var['time'])>=k_fast:
        k=((var['close'][-1]-min(var['low'][-k_fast:]))/(max(var['high'][-k_fast:])-min(var['low'][-k_fast:])))*100
    else:
        k=None
    var['k_fast'].append(k)

    #slow:
    if len(var['k_fast'])>=k_fast+d_slow:
        d=np.mean(var['k_fast'][-d_slow:])
    else:
        d=None
    var['d_slow'].append(d)

    #slow slow:
    if len(var['d_slow'])>=k_fast+d_slow+dd_slow:
        dd=np.mean(var['d_slow'][-dd_slow:])
    else:
        dd=None
    var['dd_slow'].append(dd)

def stochastic_pandas(k_fast,d_slow,dd_slow,var):

    df=pd.DataFrame(var)

    min_low=df['low'].rolling(window=k_fast,min_periods=k_fast).min()
    max_high=df['high'].rolling(window=k_fast,min_periods=k_fast).max()

    df['k_fast']=((df['close']-min_low)/(max_high-min_low))*100
    df['d_slow']=df['k_fast'].rolling(window=d_slow,min_periods=d_slow).mean()
    df['dd_slow']=df['d_slow'].rolling(window=dd_slow,min_periods=dd_slow).mean()

    for i in ['k_fast','d_slow','dd_slow']:
        var[i]=df[i].tolist()
