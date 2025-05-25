import numpy as np
import pandas as pd

def StcHma_dict(n1,n2,n3,n4,var):

    raws=[f'raw{n1}',f'raw{n2}','k_raw','d_raw']
    hmas=[f'hma{n1}',f'hma{n2}','d_macd','dd_macd']

    for i in raws+hmas+['macd','k_macd']:
        if i not in var:
            var[i]=[]

    #HMA:
    def hma(n1,n2,price,Raw,Hma,var):
        if len(var['time'])>=n1:
            wma=sum([var[price][-n2:][j]*(j+1) for j in range(n2)])/((n2*(n2+1))/2)
            wma_half=sum([var[price][-int(n2/2):][j]*(j+1) for j in range(int(n2/2))])/((int(n2/2)*(int(n2/2)+1))/2)
            raw=2*wma_half-wma
        else:
            raw=0.0
        var[Raw].append(raw)

        if len(var['time'])>=n1+int(np.sqrt(n1)):
            hma=sum([var[Raw][-int(np.sqrt(n2)):][j]*(j+1) for j in range(int(np.sqrt(n2)))])/((int(np.sqrt(n2))*(int(np.sqrt(n2))+1))/2)
        else:
            hma=0.0
        var[Hma].append(hma)
    
    hma(n1,n1,'close',f'raw{n1}',f'hma{n1}',var)
    hma(n2,n2,'close',f'raw{n2}',f'hma{n2}',var)

    #MACD:
    macd=var[f'hma{n1}'][-1]-var[f'hma{n2}'][-1] if len(var['time'])>=n2 else 0.0
    var['macd'].append(macd)

    #STOCH MACD:
    k_macd=100*(var['macd'][-1]-min(var['macd'][-n3:]))/(max(var['macd'][-n3:])-min(var['macd'][-n3:])) if len(var['time'])>=n2+n3 else 0.0
    var['k_macd'].append(k_macd)

    #D MACD:
    hma(n2+n3+n4,n4,'k_macd','k_raw','d_macd',var)
    hma(n2+n3+2*n4,n4,'d_macd','d_raw','dd_macd',var)


def StcHma_pandas(n1,n2,n3,n4,var):

    df=pd.DataFrame(var)

    def wma(series):
        weights = np.arange(1, len(series) + 1)
        return (series * weights).sum() / weights.sum()

    for n in [n1,n2]:
        wma_n=df['close'].rolling(window=n).apply(wma,raw=True)
        wma_half_n=df['close'].rolling(window=int(n/2)).apply(wma,raw=True)
        df[f'raw{n}']=2*wma_half_n-wma_n
        df[f'hma{n}']=df[f'raw{n}'].rolling(window=int(np.sqrt(n))).apply(wma,raw=True)

    df['macd']=(df[f'hma{n1}']-df[f'hma{n2}']).where(df.index>=n2-1,0.0)

    min_macd=df['macd'].rolling(window=n3).min()
    max_macd=df['macd'].rolling(window=n3).max()
    df['k_macd']=100*(df['macd']-min_macd)/(max_macd-min_macd)

    df['raw_d']=2*df['k_macd'].rolling(window=int(n4/2)).apply(wma,raw=True)-df['k_macd'].rolling(window=n4).apply(wma,raw=True)
    df['d_macd'] = df['raw_d'].rolling(window=int(np.sqrt(n4))).apply(wma, raw=True)

    df['raw_dd']=2*df['d_macd'].rolling(window=int(n4/2)).apply(wma,raw=True)-df['d_macd'].rolling(window=n4).apply(wma,raw=True)
    df['dd_macd']=df['raw_dd'].rolling(window=int(np.sqrt(n4))).apply(wma,raw=True)

    var['dd_macd']=df['dd_macd'].tolist()



