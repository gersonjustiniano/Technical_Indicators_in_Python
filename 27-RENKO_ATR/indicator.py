import numpy as np
import pandas as pd

def RenkoAtr_dict(n,var):
    
    for i in [f'atr{n}','renko_open','renko_close']:
        if i not in var:
            var[i]=[]

    #ATR:
    if len(var['time'])==n:
        atr=var['high'][-1]-var['low'][-1]
    elif len(var['time'])>n:
        atr=(var[f'atr{n}'][-1]*(n-1)+(var['high'][-1]-var['low'][-1]))/n
    else:
        atr=None
    var[f'atr{n}'].append(atr)

    if len(var['time'])>=n:
    
        brick_size = var[f'atr{n}'][-1]


        if len(var['renko_open'])==0:
            renko_open=var['close'][-1]
            renko_close=var['close'][-1]
            var['renko_open'].append(renko_open)
            var['renko_close'].append(renko_close)
        else:
            last_close = var['close'][-1]
            last_renko_close = var['renko_close'][-1]
            
            price_diff = last_close - last_renko_close
            bricks_to_add = int(price_diff / brick_size)

            if bricks_to_add != 0:
                for _ in range(abs(bricks_to_add)):
                    direction = 1 if bricks_to_add > 0 else -1
                    new_open = var['renko_close'][-1]
                    new_close = new_open + direction * brick_size

                    var['renko_open'].append(new_open)
                    var['renko_close'].append(new_close)

def RenkoAtr_pandas(n,var):

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



