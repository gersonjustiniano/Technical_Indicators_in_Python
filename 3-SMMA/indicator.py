import numpy as np
import pandas as pd

def smma_dict(n,price,var):
    
    if f'smma{n}' not in var:
        var[f'smma{n}']=[]

    if len(var[price])==n:
        savg=np.mean(var[price][-n:])
    elif len(var[price])>n:
        savg=(var[f'smma{n}'][-1]*(n-1)+var[price][-1])/n
    elif len(var[price])<n:
        savg=None
    var[f'smma{n}'].append(savg)

def smma_pandas(n,price,var):

    df=pd.DataFrame(var)

    if f'smma{n}' not in df.columns.tolist():
        df[f'smma{n}']=None

    for idx,row in df.iterrows():
        if idx==n-1:
            df.loc[idx,f'smma{n}']=np.mean(var[price][-n:])
        elif idx>n-1:
            df.loc[idx,f'smma{n}']=(df.loc[idx-1,f'smma{n}']*(n-1)+var[price][idx])/n
        elif idx<n-1:
            df.loc[idx,f'smma{n}']=None

    return df[f'smma{n}'].tolist()
        
