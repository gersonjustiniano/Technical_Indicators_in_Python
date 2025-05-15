import numpy as np
import pandas as pd

def fisher_dict(n,var):

    for i in [f'valf{n}',f'fisher{n}',f'fisher_signal{n}']:
        if i not in var:
            var[i]=[]

    mprice=[(var['high'][-n:][i]+var['low'][-n:][i])/2 for i in range(n)] if len(var['time'])>=n else None
    min_mprice=min(mprice) if len(var['time'])>=n else None
    max_mprice=max(mprice) if len(var['time'])>=n else None
    
    if len(var['time'])==n:
        valf=0.33*2*((mprice[-1]-min_mprice)/(max_mprice-min_mprice)-0.5)
        fisher=0.5*np.log((1+valf)/(1-valf))
        fisher_signal=None
    elif len(var['time'])>n:
        valf=0.33*2*((mprice[-1]-min_mprice)/(max_mprice-min_mprice)-0.5)+0.67*var[f'valf{n}'][-1]
        fisher=0.5*np.log((1+valf)/(1-valf))+0.5*var[f'fisher{n}'][-1]
        fisher_signal=var[f'fisher{n}'][-2]
    else:
        valf=0.0
        fisher=None
        fisher_signal=None
    var[f'valf{n}'].append(valf)
    var[f'fisher{n}'].append(fisher)
    var[f'fisher_signal{n}'].append(fisher_signal)

def fisher_pandas(n,var):

    df=pd.DataFrame(var)

    df[f'valf{n}']=0.0
    df[f'fisher{n}']=None
    df[f'fisher_signal{n}']=None

    for i in range(df.shape[0]):
        mprice=((df.loc[i-n+1:i,'high']+df.loc[i-n+1:i,'low'])/2).values
        min_mprice=np.min(mprice)
        max_mprice=np.max(mprice)

        if i+1==n:
            df.at[i,f'valf{n}']=0.33*2*((mprice[-1]-min_mprice)/(max_mprice-min_mprice)-0.5)
            df.at[i,f'fisher{n}']=0.5*np.log((1+df.at[i,f'valf{n}'])/(1-df.at[i,f'valf{n}']))
            df.at[i,f'fisher_signal{n}']=None
        elif i+1>n:
            df.at[i,f'valf{n}']=0.33*2*((mprice[-1]-min_mprice)/(max_mprice-min_mprice)-0.5)+0.67*df.at[i-1,f'valf{n}']
            df.at[i,f'fisher{n}']=0.5*np.log((1+df.at[i,f'valf{n}'])/(1-df.at[i,f'valf{n}']))+0.5*df.at[i-1,f'fisher{n}']
            df.at[i,f'fisher_signal{n}']=df.at[i-2,f'fisher{n}']
    
    var[f'fisher{n}']=df[f'fisher{n}'].tolist()
    var[f'fisher_signal{n}']=df[f'fisher_signal{n}'].tolist()


