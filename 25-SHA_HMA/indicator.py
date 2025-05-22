import numpy as np
import pandas as pd

def ShaHma_dict(n,var):

    raw=['raw_open','raw_high','raw_low','raw_close']
    hma=['hma_open','hma_high','hma_low','hma_close']
    sh=['sh_open','sh_close']

    for i in raw+hma+sh:
        if i not in var:
            var[i]=[]
    
    ohlc=['open','high','low','close']

    for p in ohlc:

        #WMA:
        wma=sum([var[p][-n:][j]*(j+1) for j in range(n)])/((n*(n+1))/2) if len(var['time'])>=n else 0.0
        wma_half=sum([var[p][-int(n/2):][j]*(j+1) for j in range(int(n/2))])/((int(n/2)*(int(n/2)+1))/2) if len(var['time'])>=n else 0.0
        raw=2*wma_half-wma if len(var['time'])>=n else 0.0
        var[f'raw_{p}'].append(raw)

        #HMA:
        hma=sum([var[f'raw_{p}'][-int(np.sqrt(n)):][j]*(j+1) for j in range(int(np.sqrt(n)))])/((int(np.sqrt(n))*(int(np.sqrt(n))+1))/2) if len(var['time'])>=n+int(np.sqrt(n)) else None
        var[f'hma_{p}'].append(hma)

    #SHA:
    if len(var['time'])==n+int(np.sqrt(n)):
        sh_open=var['hma_open'][-1]
        sh_close=var['hma_close'][-1]
    elif len(var['time'])>n+int(np.sqrt(n)):
        sh_open=(var['hma_open'][-2]+var['hma_close'][-2])/2
        sh_close=(var['hma_open'][-1]+var['hma_high'][-1]+var['hma_low'][-1]+var['hma_close'][-1])/4
    else:
        sh_open=0.0
        sh_close=0.0
    var['sh_open'].append(sh_open)
    var['sh_close'].append(sh_close)

def ShaHma_pandas(n,var):

    df=pd.DataFrame(var)

    ohlc=['open','high','low','close']

    def wma(series):
        weights = np.arange(1, len(series) + 1)
        return (series * weights).sum() / weights.sum()

    for p in ohlc:
        wma_n = df[p].rolling(window=n).apply(wma, raw=True)

        half_n = int(n / 2)
        wma_half_n = df[p].rolling(window=half_n).apply(wma, raw=True)

        df[f'raw_{p}']=raw = 2 * wma_half_n - wma_n

        sqrt_n = int(np.sqrt(n))
        df[f'hma_{p}'] = df[f'raw_{p}'].rolling(window=sqrt_n).apply(wma, raw=True)

    oc=['open','close']

    for i in oc:
        df[f'sh_{i}']=0.0

    for i in range(len(df)):
        if i==n-1:
            for j in oc:
                df.at[i,f'sh_{j}']=df.at[i,f'hma_{j}']
        elif i>n-1:
            df.at[i,'sh_open']=(df.at[i-1,'hma_open']+df.at[i-1,'hma_close'])/2
            df.at[i,'sh_close']=(df.at[i,'hma_open']+df.at[i,'hma_high']+df.at[i,'hma_low']+df.at[i,'hma_close'])/4

    for i in oc:
        var[f'sh_{i}']=df[f'sh_{i}'].tolist()

    





