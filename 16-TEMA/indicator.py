import numpy as np
import pandas as pd

def tema_dict(n,var):

    for i in [f'ema{n}',f'eema{n}',f'eeema{n}',f'tema{n}']:
        if i not in var:
            var[i]=[]

    #emas:
    def emas(val1,val2,var,p):
        if len(var['time'])==p:
            ema=np.mean(var[val1][-n:])
        elif len(var['time'])>p:
            multi=2/(n+1)
            ema=(var[val1][-1]-var[val2][-1])*multi+var[val2][-1]
        else:
            ema=0.0
        var[val2].append(ema)
    emas('close',f'ema{n}',var,n)
    emas(f'ema{n}',f'eema{n}',var,2*n)
    emas(f'eema{n}',f'eeema{n}',var,3*n)

    #tema:
    if len(var['time'])>=3*n:
        tema=3*(var[f'ema{n}'][-1]-var[f'eema{n}'][-1])+var[f'eeema{n}'][-1]
    else:
        tema=None
    var[f'tema{n}'].append(tema)

def tema_pandas(n,var):

    df=pd.DataFrame(var)

    df[f'ema{n}']=df['close'].ewm(span=n,adjust=False).mean()
    df[f'eema{n}']=df[f'ema{n}'].ewm(span=n,adjust=False).mean()
    df[f'eeema{n}']=df[f'eema{n}'].ewm(span=n,adjust=False).mean()
    df[f'tema{n}']=3*(df[f'ema{n}']-df[f'eema{n}'])+df[f'eeema{n}']
    df[f'tema{n}']=df[f'tema{n}'].where(df.index>=n+1,None)

    var[f'tema{n}']=df[f'tema{n}'].tolist()
