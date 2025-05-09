import numpy as np
import pandas as pd

def smooth_heikin_dict(n,var):

    for i in ['sma_open','sma_high','sma_low','sma_close','sh_open','sh_high','sh_low','sh_close']:
        if i not in var:
            var[i]=[]

    ohlc=['open','high','low','close']

    #sma:
    for i in ohlc:
        if len(var['time'])>=n:
            sma=np.mean(var[i][-n:])
        else:
            sma=None
        var[f'sma_{i}'].append(sma)

    #smooth heikin ashi:
    if len(var['time'])==n:
        sh_open=var[f'sma_open'][-1]
        sh_high=var[f'sma_high'][-1]
        sh_low=var[f'sma_low'][-1]
        sh_close=var[f'sma_close'][-1]
    elif len(var['time'])>n:
        sh_open=(var['sma_open'][-2]+var['sma_close'][-2])/2
        sh_high=max([var['sma_high'][-1],var['sma_open'][-1],var['sma_close'][-1]])
        sh_low=min([var['sma_low'][-1],var['sma_open'][-1],var['sma_close'][-1]])
        sh_close=(var['sma_open'][-1]+var['sma_high'][-1]+var['sma_low'][-1]+var['sma_close'][-1])/4
    elif len(var['time'])<n:
        sh_open=0
        sh_high=0
        sh_low=0
        sh_close=0
    var['sh_open'].append(sh_open)
    var['sh_high'].append(sh_high)
    var['sh_low'].append(sh_low)
    var['sh_close'].append(sh_close)


def smooth_heikin_pandas(n,var):

    df=pd.DataFrame(var)
    
    ohlc=['open','high','low','close']

    #sma:
    for i in ohlc:
        df[f'sma_{i}']=df[i].rolling(window=n).mean()
        df[f'sh_{i}']=0.0

    #smooth heikin ashi:
    for i in range(len(df)):
        if i==n-1:
            for j in ohlc:
                df.at[i,f'sh_{j}']=df.at[i,f'sma_{j}']
        elif i>n-1:
            df.at[i,'sh_open']=(df.at[i-1,'sma_open']+df.at[i-1,'sma_close'])/2
            df.at[i,'sh_high']=max(df.at[i,'sma_high'],df.at[i,'sma_open'],df.at[i,'sma_close'])
            df.at[i,'sh_low']=min(df.at[i,'sma_low'],df.at[i,'sma_open'],df.at[i,'sma_close'])
            df.at[i,'sh_close']=(df.at[i,'sma_open']+df.at[i,'sma_high']+df.at[i,'sma_low']+df.at[i,'sma_close'])/4

    for i in ['sh_open','sh_high','sh_low','sh_close']:
        var[i]=df[i].tolist()
