import numpy as np
import pandas as pd

def rsi_dict(n,price,var):

    if 'gain' and 'loss' and 'avg_gain' and 'avg_loss' and 'rsi' not in var:
        for i in ['gain','loss','avg_gain','avg_loss','rsi']:
            var[i]=[]

    if len(var['time'])>1:
        e=var[price][-1]-var[price][-2]
        if e>0:
            var['gain'].append(abs(e))
            var['loss'].append(0)
        elif e<0:
            var['gain'].append(0)
            var['loss'].append(abs(e))
        elif e==0:
            var['gain'].append(0)
            var['loss'].append(0)

    if len(var['time'])==n:
        g=np.mean(var['gain'][-n:])
        l=np.mean(var['loss'][-n:])
    elif len(var['time'])>n:
        g=(var['avg_gain'][-1]*(n-1)+var['gain'][-1])/n
        l=(var['avg_loss'][-1]*(n-1)+var['loss'][-1])/n
    else:
        g=0
        l=0
    var['avg_gain'].append(g)
    var['avg_loss'].append(l)

    if len(var['time'])>=0:
        if var['avg_loss'][-1]==0:
            RSI=None
        else:
            rs=var['avg_gain'][-1]/var['avg_loss'][-1]
            RSI=100-100/(1+rs)
        var['rsi'].append(RSI)
    else:
        var['rsi'].append(None)

def rsi_pandas(n,price,var):

    df=pd.DataFrame(var)

    df['price_diff']=df[price].diff()
    df['gain']=df['price_diff'].where(df['price_diff']>0,0)
    df['loss']=abs(df['price_diff'].where(df['price_diff']<0,0))
    df['gain']=df['gain'].fillna(0)
    df['loss']=df['loss'].fillna(0)

    df['avg_gain']=df['gain'].rolling(window=n,min_periods=1).mean()
    df['avg_loss']=df['loss'].rolling(window=n,min_periods=1).mean()

    df['rs']=df['avg_gain']/df['avg_loss']
    df['rsi']=100-100/(1+df['rs'])

    var['rsi']=df['rsi'].tolist()
