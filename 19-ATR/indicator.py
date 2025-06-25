import numpy as np
import pandas as pd

def atr_dict(n,var):

    if f'atr{n}' not in var:
        var[f'atr{n}']=[]

    if len(var['time'])==n:
        tr=max(var['high'][-1]-var['low'][-1],abs(var['high'][-1]-var['close'][-2]),abs(var['low'][-1]-var['close'][-2]))
        atr=tr
    elif len(var['time'])>n:
        tr=max(var['high'][-1]-var['low'][-1],abs(var['high'][-1]-var['close'][-2]),abs(var['low'][-1]-var['close'][-2]))
        atr=(var[f'atr{n}'][-1]*(n-1)+tr)/n
    else:
        atr=None

    var[f'atr{n}'].append(atr)

def atr_pandas(n,var):

    df=pd.DataFrame(var)

    df[f'atr{n}']=None

    for i in range(df.shape[0]):
        if i+1==n:
            tr=max(df.at[i,'high']-df.at[i,'low'],abs(df.at[i,'high']-df.at[i-1,'close']),abs(df.at[i,'low']-df.at[i-1,'close']))
            df.at[i,f'atr{n}']=tr
        elif i+1>n:
            tr=max(df.at[i,'high']-df.at[i,'low'],abs(df.at[i,'high']-df.at[i-1,'close']),abs(df.at[i,'low']-df.at[i-1,'close']))
            df.at[i,f'atr{n}']=(df.at[i-1,f'atr{n}']*(n-1)+tr)/n

    var[f'atr{n}']=df[f'atr{n}'].tolist()


