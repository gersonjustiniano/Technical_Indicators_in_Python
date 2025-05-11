import numpy as np
import pandas as pd

def wma_dict(n,var):

    if f'wma{n}' not in var:
        var[f'wma{n}']=[]

    if len(var['time'])>=n:
        wma=sum([var['close'][-n:][i]*(i+1) for i in range(n)])/((n*(n+1))/2)
    else:
        wma=None
    var[f'wma{n}'].append(wma)


def wma_pandas(n,var):

    df=pd.DataFrame(var)

    weights=np.arange(1,n+1)

    df[f'wma{n}']=df['close'].rolling(window=n).apply(lambda x: np.dot(x,weights)/weights.sum(),raw=True)
    df[f'wma{n}']=df[f'wma{n}'].where(df.index>=n-1,None)

    var[f'wma{n}']=df[f'wma{n}'].tolist()


