import numpy as np
import pandas as pd

def dema_dict(n,var):

    for i in [f'ema{n}',f'eema{n}',f'dema{n}']:
        if i not in var:
            var[i]=[]

    #ema:
    if len(var['time'])==n:
        ema=np.mean(var['close'][-n:])
    elif len(var['time'])>n:
        multi=2/(n+1)
        ema=(var['close'][-1]-var[f'ema{n}'][-1])*multi+var[f'ema{n}'][-1]
    else:
        ema=0.0
    var[f'ema{n}'].append(ema)

    #ema of ema:
    if len(var['time'])==2*n:
        eema=np.mean(var[f'ema{n}'][-n:])
    elif len(var['time'])>2*n:
        multi=2/(n+1)
        eema=(var[f'ema{n}'][-1]-var[f'eema{n}'][-1])*multi+var[f'eema{n}'][-1]
    else:
        eema=0.0
    var[f'eema{n}'].append(eema)

    #dema:
    if len(var['time'])>=2*n:
        dema=2*var[f'ema{n}'][-1]-var[f'eema{n}'][-1]
    else:
        dema=None
    var[f'dema{n}'].append(dema)


def dema_pandas(n,var):

    df=pd.DataFrame(var)

    df[f'ema{n}']=0.0
    df[f'eema{n}']=0.0
    df[f'dema{n}']=None

    for i in range(df.shape[0]):
        #ema:
        if i+1==n:
            df.at[i,f'ema{n}']=df['close'].iloc[i+1-n:i+1].mean()
        elif i+1>n:
            multi=2/(n+1)
            df.at[i,f'ema{n}']=(df.at[i,'close']-df.at[i-1,f'ema{n}'])*multi+df.at[i-1,f'ema{n}']

        #ema of ema:
        if i+1==2*n:
            df.at[i,f'eema{n}']=df[f'ema{n}'].iloc[i+1-n:i+1].mean()
        elif i+1>2*n:
            multi=2/(n+1)
            df.at[i,f'eema{n}']=(df.at[i,f'ema{n}']-df.at[i-1,f'eema{n}'])*multi+df.at[i-1,f'eema{n}']

        #dema:
        if i+1>=2*n:
            df.at[i,f'dema{n}']=2*df.at[i,f'ema{n}']-df.at[i,f'eema{n}'] 


    var[f'dema{n}']=df[f'dema{n}'].tolist()

