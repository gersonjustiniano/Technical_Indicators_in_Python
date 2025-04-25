import numpy as np

def sma_dict(n,price,var):
    
    if f'sma{n}' not in var:
        var[f'sma{n}']=[]

    if len(var[price])>=n:
        avg=np.mean(var[price][-n:])
        var[f'sma{n}'].append(avg)
    else:
        var[f'sma{n}'].append(None)

def sma_pandas(n,price,var):
    row,dict_data=var
    idx=row.name

    if idx>=n-1:
        avg=np.mean(dict_data[price][idx-n+1:idx+1])
        return avg
    else:
        return None
        
