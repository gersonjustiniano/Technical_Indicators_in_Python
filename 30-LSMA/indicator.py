import numpy as np
import pandas as pd

def lsma_dict(price,n,var):
    
    if f'lsma{n}' not in var:
        var[f'lsma{n}']=[]

    if len(var['time'])>=n:
        sum_n=n*(n+1)/2
        sum_nsquare=n*(n+1)*(2*n+1)/6
        sum_price=sum(var[price][-n:])
        sum_nprice=sum([(i+1)*var[price][-n:][i] for i in range(n)])

        b=(n*sum_nprice-sum_n*sum_price)/(n*sum_nsquare-sum_n**2)
        a=(sum_price-b*sum_n)/n
        lsma=a+b*n
    else:
        lsma=None
    var[f'lsma{n}'].append(lsma)


def lsma_pandas(price,n,var):

    df=pd.DataFrame(var)

    x=np.arange(1,n+1)
    sum_x=x.sum()
    sum_x2=(x**2).sum()

    def lsma(y):
        sum_y=y.sum()
        sum_xy=(x*y).sum()
        b=(n*sum_xy-sum_x*sum_y)/(n*sum_x2-sum_x**2)
        a=(sum_y-b*sum_x)/n
        return a+b*n
    
    df[f'lsma{n}']=df[price].rolling(window=n).apply(lsma,raw=True)

    var[f'lsma{n}']=df[f'lsma{n}'].tolist()
