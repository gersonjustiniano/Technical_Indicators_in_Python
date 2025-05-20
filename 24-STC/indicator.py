import numpy as np
import pandas as pd

def stc_dict(n1,n2,n3,n4,var):

    for i in [f'ema{n1}',f'ema{n2}','macd','k_macd','d_macd','dd_macd']:
        if i not in var:
            var[i]=[]

    #ema:
    def ema(n,val1,val2,var):
        if len(var['time'])==n:
            ema=np.mean(var[val1][-n:])
        elif len(var['time'])>n:
            multi=2/(n+1)
            ema=(var[val1][-1]-var[val2][-1])*multi+var[val2][-1]
        else:
            ema=0.0
        var[val2].append(ema)
    ema(n1,'close',f'ema{n1}',var)
    ema(n2,'close',f'ema{n2}',var)

    #macd:
    macd=var[f'ema{n1}'][-1]-var[f'ema{n2}'][-1] if len(var['time'])>=n2 else 0.0
    var['macd'].append(macd)

    #k macd:
    k_macd=100*(var['macd'][-1]-min(var['macd'][-n3:]))/(max(var['macd'][-n3:])-min(var['macd'][-n3:])) if len(var['time'])>=n2+n3 else 0.0
    var['k_macd'].append(k_macd)

    #d macd:
    if len(var['time'])==n2+n3+n4:
        d_macd=np.mean(var['k_macd'][-n4:])
    elif len(var['time'])>n2+n3+n4:
        d_multi=2/(n4+1)
        d_macd=(var['k_macd'][-1]-var['d_macd'][-1])*d_multi+var['d_macd'][-1]
    else:
        d_macd=0.0
    var['d_macd'].append(d_macd)

    #dd macd:
    if len(var['time'])==n2+n3+2*n4:
        dd_macd=np.mean(var['d_macd'][-n4:])
    elif len(var['time'])>n2+n3+2*n4:
        dd_multi=2/(n4+1)
        dd_macd=(var['d_macd'][-1]-var['dd_macd'][-1])*dd_multi+var['dd_macd'][-1]
    else:
        dd_macd=None
    var['dd_macd'].append(dd_macd)


def stc_pandas(n1,n2,n3,n4,var):

    df=pd.DataFrame(var)

    df[f'ema{n1}']=df['close'].ewm(span=n1,adjust=False).mean().where(df.index>=n1-1,0.0)
    df[f'ema{n2}']=df['close'].ewm(span=n2,adjust=False).mean().where(df.index>=n2-1,0.0)
    
    df['macd']=(df[f'ema{n1}']-df[f'ema{n2}']).where(df.index>=n2-1,0.0)
    
    min_macd=df['macd'].rolling(window=n3).min()
    max_macd=df['macd'].rolling(window=n3).max()
    df['k_macd']=100*(df['macd']-min_macd)/(max_macd-min_macd)

    df['d_macd']=df['k_macd'].ewm(span=n4,adjust=False).mean().where(df.index>=n2+n3+n4-1,0.0)
    df['dd_macd']=df['d_macd'].ewm(span=n4,adjust=False).mean().where(df.index>=n2+n3+2*n4-1,np.nan)

    var['dd_macd']=df['dd_macd'].tolist()




