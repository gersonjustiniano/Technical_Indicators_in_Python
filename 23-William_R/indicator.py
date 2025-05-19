import numpy as np
import pandas as pd

def williamR_dict(n,var):

    if f'willR{n}' not in var:
        var[f'willR{n}']=[]

    if len(var['time'])>=n:
        min_low=min(var['low'][-n:])
        max_high=max(var['high'][-n:])
        willR=-100*(max_high-var['close'][-1])/(max_high-min_low)
    else:
        willR=None
    var[f'willR{n}'].append(willR)

def williamR_pandas(n,var):

    df=pd.DataFrame(var)

    min_low=df['low'].rolling(window=n).min()
    max_high=df['high'].rolling(window=n).max()
    df[f'willR{n}']=-100*(max_high-df['close'])/(max_high-min_low)

    var[f'willR{n}']=df[f'willR{n}'].tolist()





