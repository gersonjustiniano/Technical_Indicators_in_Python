import numpy as np
import pandas as pd

def fractals_dict(n,var):

    for n in ['up','down']:
        if n not in var:
            var[n]=[]

    if len(var['time'])>=2*n+1:
        
        up=[True if var['high'][-n-1]>var['high'][-n-i-2] and var['high'][-n-1]>var['high'][-n+i] else False for i in range(n)]
        down=[True if var['low'][-n-1]<var['low'][-n-i-2] and var['low'][-n-1]<var['low'][-n+i] else False for i in range(n)]
        if all(up):
            var['up'].append([var['time'][-n-1],var['high'][-n-1]])
        elif all(down):
            var['down'].append([var['time'][-n-1],var['low'][-n-1]])

        '''
        #this also works:

        up=True
        down=True

        for i in range(-n,n+1):
            if var['high'][-n-1]<var['high'][-n-1+i] and i!=0:
                up=False
        for i in range(-n,n+1):
            if var['low'][-n-1]>var['low'][-n-1+i] and i!=0:
                down=False

        if up:
            var['up'].append([var['time'][-n-1],var['high'][-n-1]])
        elif down:
            var['down'].append([var['time'][-n-1],var['low'][-n-1]])
        '''

def fractals_pandas(n,var):

    df=pd.DataFrame(var)

    df['fractal']='-'

    for i,_ in df.iterrows():
        if n<=i<len(df)-n:
            Up=[True if df.loc[i,'high']>df.loc[i+j,'high'] and df.loc[i,'high']>df.loc[i-j,'high'] else False for j in range(1,n+1)]
            Down=[True if df.loc[i,'low']<df.loc[i+j,'low'] and df.loc[i,'low']<df.loc[i-j,'low'] else False for j in range(1,n+1)]
            if all(Up):
                df.loc[i,'fractal']='up'
            elif all(Down):
                df.loc[i,'fractal']='down'

    up=[[df.loc[i,'time'],df.loc[i,'high']] for i,_ in df.iterrows() if df.loc[i,'fractal']=='up']
    down=[[df.loc[i,'time'],df.loc[i,'low']] for i,_ in df.iterrows() if df.loc[i,'fractal']=='down']
    var['up']=up
    var['down']=down


