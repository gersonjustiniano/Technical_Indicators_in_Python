import numpy as np
import pandas as pd

def macd_dict(ema_fast,ema_slow,signal,price,var):

    if f'ema{ema_fast}' and f'ema{ema_slow}' and 'macd' and 'signal_macd' and 'macd_histogram' not in var:
        for i in [f'ema{ema_fast}',f'ema{ema_slow}','macd','signal_macd','macd_histogram']:
            var[i]=[]

    #emas:
    for n in [ema_fast,ema_slow]:
        if len(var['time'])==n:
            ema=np.mean(var[price][-n:])
        elif len(var['time'])>n:
            multi=2/(n+1)
            ema=(var[price][-1]-var[f'ema{n}'][-1])*multi+var[f'ema{n}'][-1]
        elif len(var['time'])<n:
            ema=0
        var[f'ema{n}'].append(ema)

    #macd:
    if len(var[f'ema{ema_slow}'])>=ema_slow:
        macd=var[f'ema{ema_fast}'][-1]-var[f'ema{ema_slow}'][-1]
    else:
        macd=None
    var['macd'].append(macd)

    #signal:
    if len(var['macd'])==ema_slow+signal:
        ema_macd=np.mean(var['macd'][-signal:])
    elif len(var['macd'])>ema_slow+signal:
        multi_macd=2/(signal+1)
        ema_macd=(var['macd'][-1]-var['signal_macd'][-1])*multi_macd+var['signal_macd'][-1]
    elif len(var['macd'])<ema_slow+signal:
        ema_macd=None
    var['signal_macd'].append(ema_macd)

    #macd histogram:
    if len(var['signal_macd'])>=ema_slow+signal:
        macd_histo=var['macd'][-1]-var['signal_macd'][-1]
    else:
        macd_histo=0
    var['macd_histogram'].append(macd_histo)

def macd_pandas(ema_fast,ema_slow,signal,price,var):

    df=pd.DataFrame(var)

    #emas:
    for n in [ema_fast,ema_slow]:
        df[f'ema{n}']=df[price].ewm(span=n,adjust=False).mean()
        df[f'ema{n}']=df[f'ema{n}'].where(df.index>=ema_slow-1,0)

    #macd:
    df['macd']=df[f'ema{ema_fast}']-df[f'ema{ema_slow}']
    df['macd']=df['macd'].where(df.index>=ema_slow-1,None)

    #signal:
    df['signal_macd']=df['macd'].ewm(span=signal,adjust=False).mean()

    #histogram:
    df['macd_histogram']=df['macd']-df['signal_macd']

    for i in ['macd','signal_macd','macd_histogram']:
        var[i]=df[i].tolist()
