import numpy as np
import pandas as pd

def atr_dict(n,var):

    if f'atr{n}' not in var:
        var[f'atr{n}']=[]

    if len(var['time'])==n:
        atr=var['high'][-1]-var['low'][-1]
    elif len(var['time'])>n:
        atr=(var[f'atr{n}'][-1]*(n-1)+(var['high'][-1]-var['low'][-1]))/n
    else:
        atr=None

    var[f'atr{n}'].append(atr)

def atr_pandas(n,var):

    df=pd.DataFrame(var)

    df[f'atr{n}']=None

    for i in range(df.shape[0]):
        if i+1==n:
            df.at[i,f'atr{n}']=df.at[i,'high']-df.at[i,'low']
        elif i+1>n:
            df.at[i,f'atr{n}']=(df.at[i-1,f'atr{n}']*(n-1)+(df.at[i,'high']-df.at[i,'low']))/n

    var[f'atr{n}']=df[f'atr{n}'].tolist()


