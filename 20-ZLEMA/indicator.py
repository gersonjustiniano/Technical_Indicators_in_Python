import numpy as np
import pandas as pd

def zlema_dict(n,var):

    for i in [f'price_lag{n}',f'zlema{n}']:
        if i not in var:
            var[i]=[]

    #price lag:
    if len(var['time'])>=n:
        lag=int((n-1)/2)
        price_lag=var['close'][-1]+(var['close'][-1]-var['close'][-lag])
    else:
        price_lag=0.0
    var[f'price_lag{n}'].append(price_lag)

    #zlema:
    if len(var['time'])==2*n:
        zlema=np.mean(var[f'price_lag{n}'][-n:])
    elif len(var['time'])>2*n:
        multi=2/(n+1)
        zlema=(var[f'price_lag{n}'][-1]-var[f'zlema{n}'][-1])*multi+var[f'zlema{n}'][-1]
    else:
        zlema=np.nan
    var[f'zlema{n}'].append(zlema)

def zlema_pandas(n,var):

    df=pd.DataFrame(var)

    #price lag:
    lag = (n - 1) // 2
    df[f'price_lag{n}'] = df['close'].shift(lag)
    df[f'price_adjusted{n}'] = 2 * df['close'] - df[f'price_lag{n}']
    df[f'zlema{n}'] = df[f'price_adjusted{n}'].ewm(span=n, adjust=False).mean()
    
    var[f'zlema{n}']=df[f'zlema{n}'].tolist()


