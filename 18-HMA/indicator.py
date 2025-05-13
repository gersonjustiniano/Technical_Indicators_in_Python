import numpy as np
import pandas as pd

def hma_dict(n,var):

    for i in [f'raw{n}',f'hma{n}']:
        if i not in var:
            var[i]=[]

    #wma:
    if len(var['time'])>=n:
        wma=sum([var['close'][-n:][j]*(j+1) for j in range(n)])/((n*(n+1))/2)
        wma_half=sum([var['close'][-int(n/2):][j]*(j+1) for j in range(int(n/2))])/((int(n/2)*(int(n/2)+1))/2)
        raw=2*wma_half-wma
    else:
        raw=0.0
    var[f'raw{n}'].append(raw)

    #hma:
    if len(var['time'])>=n+int(np.sqrt(n)):
        hma=sum([var[f'raw{n}'][-int(np.sqrt(n)):][j]*(j+1) for j in range(int(np.sqrt(n)))])/((int(np.sqrt(n))*(int(np.sqrt(n))+1))/2)
    else:
        hma=None
    var[f'hma{n}'].append(hma)

def hma_pandas(n,var):

    df=pd.DataFrame(var)

    def wma(series):
        weights = np.arange(1, len(series) + 1)
        return (series * weights).sum() / weights.sum()

    wma_n = df['close'].rolling(window=n).apply(wma, raw=True)
    
    half_n = int(n / 2)
    wma_half_n = df['close'].rolling(window=half_n).apply(wma, raw=True)

    raw = 2 * wma_half_n - wma_n
    df[f'raw{n}'] = raw

    sqrt_n = int(np.sqrt(n))
    df[f'hma{n}'] = df[f'raw{n}'].rolling(window=sqrt_n).apply(wma, raw=True)

    var[f'hma{n}']=df[f'hma{n}'].tolist()



