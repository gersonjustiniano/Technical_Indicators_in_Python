import numpy as np
import pandas as pd

def alligator_dict(lst,var):

    for n in ['lips','teeth','jaw']:
        if n not in var:
            var[n]=[]

    for n in lst:
        if len(var['time'])==n:
            mprice=[(var['high'][-n:][j]+var['low'][-n:][j])/2 for j in range(n)]
            croc=np.mean(mprice)
        elif len(var['time'])>n:
            croc_prev=var[{lst[0]:'lips',lst[1]:'teeth',lst[2]:'jaw'}[n]][-1]
            croc=(croc_prev*(n-1)+(var['high'][-1]+var['low'][-1])/2)/n
        elif len(var['time'])<n:
            croc=None
        smma={lst[0]:'lips',lst[1]:'teeth',lst[2]:'jaw'}[n]
        var[smma].append(croc)

def alligator_pandas(lst,var):

    df=pd.DataFrame(var)

    for i in ['lips','teeth','jaw']:
        df[i]=None

    for n in lst:
        smma={lst[0]:'lips',lst[1]:'teeth',lst[2]:'jaw'}[n]
        for i,row in df.iterrows():
            if i==n-1:
                mprices=[(df.loc[j,'high']+df.loc[j,'low'])/2 for j in range(i-n+1,i+1)]
                df.loc[i,smma]=np.mean(mprices)
            elif i>n-1:
                mprice=(df.loc[i,'high']+df.loc[i,'low'])/2
                df.loc[i,smma]=(df.loc[i-1,smma]*(n-1)+mprice)/n
            elif i<n-1:
                df.loc[i,smma]=None

    for i in ['lips','teeth','jaw']:
        var[i]=df[i].tolist()


