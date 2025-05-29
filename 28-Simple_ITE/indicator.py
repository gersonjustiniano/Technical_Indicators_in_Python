import numpy as np
import pandas as pd

def SimpleITE_dict(price,var):
    
    if 'simple_ite' not in var:
        var['simple_ite']=[]

    if len(var['time'])>=3:
        simple_ite=(var[price][-1]+2*var[price][-2]+var[price][-3])/4
    else:
        simple_ite=None
    var['simple_ite'].append(simple_ite)

def SimpleITE_pandas(price,var):

    df=pd.DataFrame(var)

    df['simple_ite']=(df[price]+2*df[price].shift(1)+df[price].shift(2))/4

    var['simple_ite']=df['simple_ite'].tolist()

    


