import numpy as np
import pandas as pd

def bollinger_dict(n,s,price,var):
    
    if 'up_BB' and 'down_BB' and 'avg_BB' not in var:
        var['avg_BB']=[]
        var['up_BB']=[]
        var['down_BB']=[]
        
    if len(var[price])>=n:
        avg=np.mean(var[price][-n:])
        std=np.std(var[price][-n:])
        upBB=avg+s*std
        downBB=avg-s*std
        var['avg_BB'].append(avg)
        var['up_BB'].append(upBB)
        var['down_BB'].append(downBB)
    elif len(var[price])<n:
        var['avg_BB'].append(None)
        var['up_BB'].append(None)
        var['down_BB'].append(None)

def bollinger_pandas(n,s,price,var):

    df=pd.DataFrame(var)

    df['avg_BB']=df[price].rolling(window=n,min_periods=n).mean()
    df['std_BB']=df[price].rolling(window=n,min_periods=n).std()
    df['up_BB']=df['avg_BB']+s*df['std_BB']
    df['down_BB']=df['avg_BB']-s*df['std_BB']

    for i in ['avg_BB','up_BB','down_BB']:
        var[i]=df[i].tolist()
