import numpy as np
import pandas as pd

def ema_dict(n,price,var):
    
    if f'ema{n}' not in var:
        var[f'ema{n}']=[]

    if len(var[price])==n:
        ema=np.mean(var[price][-n:])
    elif len(var[price])>n:
        multi=2/(n+1)
        ema=(var[price][-1]-var[f'ema{n}'][-1])*multi+var[f'ema{n}'][-1]
    elif len(var[price])<n:
        ema=None
    var[f'ema{n}'].append(ema)

def ema_pandas(n,price,var):

    df=pd.DataFrame(var)

    if f'ema{n}' not in df.columns.tolist():
        df[f'ema{n}']=None

    for idx,row in df.iterrows():
        if idx==n-1:
            df.loc[idx,f'ema{n}']=np.mean(var[price][-n:])
        elif idx>n-1:
            multi=2/(n+1)
            df.loc[idx,f'ema{n}']=(var[price][idx]-df.loc[idx-1,f'ema{n}'])*multi+df.loc[idx-1,f'ema{n}']
        elif idx<n-1:
            df.loc[idx,f'ema{n}']=None

    return df[f'ema{n}'].tolist()
        
