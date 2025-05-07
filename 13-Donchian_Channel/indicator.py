import numpy as np
import pandas as pd

def donchian_dict(n,var):

    for i in ['upper_band','lower_band','median_price']:
        if i not in var:
            var[i]=[]

    upper_band=max(var['high'][-n:]) if len(var['time'])>=n else None
    lower_band=min(var['low'][-n:]) if len(var['time'])>=n else None
    median_price=(max(var['high'][-n:])+min(var['low'][-n:]))/2 if len(var['time'])>=n else None
    var['upper_band'].append(upper_band)
    var['lower_band'].append(lower_band)
    var['median_price'].append(median_price)

def donchian_pandas(n,var):

    df=pd.DataFrame(var)
    
    df['upper_band']=df['high'].rolling(window=n).max()
    df['lower_band']=df['low'].rolling(window=n).min()
    df['median_price']=(df['upper_band']+df['lower_band'])/2

    for i in ['upper_band','lower_band','median_price']:
        var[i]=df[i].tolist()
