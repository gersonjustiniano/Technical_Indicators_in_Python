import numpy as np
import pandas as pd

def cci_dict(n,var):

    for i in [f'cci{n}',f'avg_Tprice{n}']:
        if i not in var:
            var[i]=[]

    Tprice=[(var['high'][-n:][i]+var['low'][-n:][i]+var['close'][-n:][i])/3 for i in range(n)] if len(var['time'])>=n else None
    avg_Tprice=np.mean(Tprice) if len(var['time'])>=n else None
    var[f'avg_Tprice{n}'].append(avg_Tprice)

    if len(var['time'])>2*n:
        mean_dev=sum([abs(Tprice[i]-var[f'avg_Tprice{n}'][-n:][i]) for i in range(n)])/n
        cci=(Tprice[-1]-var[f'avg_Tprice{n}'][-1])/(0.015*mean_dev)
    else:
        cci=None
    var[f'cci{n}'].append(cci)

def cci_pandas(n,var):

    df=pd.DataFrame(var)

    df['Tprice']=(df['high']+df['low']+df['close'])/3
    df[f'avg_Tprice{n}']=df['Tprice'].rolling(window=n).mean()

    def mean_deviation(x):
        mean=x.mean()
        return np.mean(np.abs(x-mean))

    df['mean_dev'] = df['Tprice'].rolling(window=n).apply(mean_deviation, raw=True)
    df[f'cci{n}'] = (df['Tprice'] - df[f'avg_Tprice{n}']) / (0.015 * df['mean_dev'])

    var[f'cci{n}']=df[f'cci{n}'].tolist()



