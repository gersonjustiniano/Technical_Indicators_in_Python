import numpy as np
import pandas as pd

def awesome_dict(fast,slow,var):

    if 'mprice' and f'sma{fast}' and f'sma{slow}' and 'ao' not in var:
        for i in ['mprice',f'sma{fast}',f'sma{slow}','ao']:
            var[i]=[]

    #midle price:
    mprice=(var['high'][-1]+var['low'][-1])/2
    var['mprice'].append(mprice)

    #sma's:
    for n in [fast,slow]:
        if len(var['time'])>=n:
            avg_ao=np.mean(var['mprice'][-n:])
        else:
            avg_ao=0
        var[f'sma{n}'].append(avg_ao)

    #ao:
    if len(var['time'])>=slow:
        ao=var[f'sma{fast}'][-1]-var[f'sma{slow}'][-1]
    else:
        ao=0
    var['ao'].append(ao)

def awesome_pandas(fast,slow,var):

    df=pd.DataFrame(var)

    #midle price:
    df['mprice']=(df['high']+df['low'])/2

    #sma's:
    df[f'sma{fast}']=df['mprice'].rolling(window=fast).mean()
    df[f'sma{slow}']=df['mprice'].rolling(window=slow).mean()

    #ao:
    df['ao']=df[f'sma{fast}']-df[f'sma{slow}']
    df['ao']=df['ao'].where(df.index>=slow-1,None)

    for i in ['mprice',f'sma{fast}',f'sma{slow}','ao']:
        var[i]=df[i].tolist()

