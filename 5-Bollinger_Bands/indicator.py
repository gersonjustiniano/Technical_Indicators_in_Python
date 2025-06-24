import numpy as np
import pandas as pd

def bollinger_dict(n,s,price,var):
    
    for i in ['up_BB','down_BB','avg_BB','percentB','bandWidth']:
        if i not in var:
            var[i]=[]
        
    #BOLLINGER BAND:
    if len(var[price])>=n:
        avg=np.mean(var[price][-n:])
        std=np.std(var[price][-n:])
        upBB=avg+s*std
        downBB=avg-s*std
    else:
        avg=np.nan
        upBB=np.nan
        downBB=np.nan
    var['avg_BB'].append(avg)
    var['up_BB'].append(upBB)
    var['down_BB'].append(downBB)

    #PERCENT B:
    if len(var[price])>=n:
        percentB=(var[price][-1]-var['down_BB'][-1])/(var['up_BB'][-1]-var['down_BB'][-1])
    else:
        percentB=np.nan
    var['percentB'].append(percentB)

    #BAND WIDTH:
    if len(var['time'])>=n:
        bandWidth=(var['up_BB'][-1]-var['down_BB'][-1])/var['avg_BB'][-1]
    else:
        bandWidth=np.nan
    var['bandWidth'].append(bandWidth)

def bollinger_pandas(n,s,price,var):

    df=pd.DataFrame(var)

    df['avg_BB']=df[price].rolling(window=n,min_periods=n).mean()
    df['std_BB']=df[price].rolling(window=n,min_periods=n).std()
    df['up_BB']=df['avg_BB']+s*df['std_BB']
    df['down_BB']=df['avg_BB']-s*df['std_BB']
    df['percentB']=(df[price]-df['down_BB'])/(df['up_BB']-df['down_BB'])
    df['bandWidth']=(df['up_BB']-df['down_BB'])/df['avg_BB']
    
    for i in ['avg_BB','up_BB','down_BB','percentB','bandWidth']:
        var[i]=df[i].tolist()
