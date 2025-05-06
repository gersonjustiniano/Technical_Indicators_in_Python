import numpy as np
import pandas as pd

def heikin_dict(var):

    for n in ['h_open','h_high','h_low','h_close']:
        if n not in var:
            var[n]=[]
    
    h_open=var['open'][-1] if len(var['time'])==1 else (var['h_open'][-1]+var['h_close'][-1])/2
    h_high=var['high'][-1] if len(var['time'])==1 else max([var['high'][-1],var['h_open'][-1],var['h_close'][-1]])
    h_low=var['low'][-1] if len(var['time'])==1 else min([var['low'][-1],var['h_open'][-1],var['h_close'][-1]])
    h_close=var['close'][-1] if len(var['time'])==1 else (var['open'][-1]+var['high'][-1]+var['low'][-1]+var['close'][-1])/4

    var['h_open'].append(h_open)
    var['h_high'].append(h_high)
    var['h_low'].append(h_low)
    var['h_close'].append(h_close)


def heikin_pandas(var):

    df=pd.DataFrame(var)
    
    df['h_open']=0.0
    df['h_high']=0.0
    df['h_low']=0.0
    df['h_close']=(df['open']+df['high']+df['low']+df['close'])/4

    for i in range(len(df)):
        if i==0:
            df.at[i,'h_open']=df.at[i,'open']
        else:
            df.at[i,'h_open']=(df.at[i-1,'h_open']+df.at[i-1,'h_close'])/2

        df.at[i,'h_high']=max(df.at[i,'high'],df.at[i,'h_open'],df.at[i,'h_close'])
        df.at[i,'h_low']=min(df.at[i,'low'],df.at[i,'h_open'],df.at[i,'h_close'])

    for i in ['h_open','h_high','h_low','h_close']:
        var[i]=df[i].tolist()


