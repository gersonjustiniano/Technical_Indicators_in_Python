import numpy as np
import pandas as pd

def SmoothITE_dict(price,alpha,var):
    
    if 'smooth_ite' not in var:
        var['smooth_ite']=[]

    if len(var['time'])>=2:
        smooth_ite=alpha*(var[price][-1]+var[price][-2])/2+(1-alpha)*var['smooth_ite'][-1]
    else:
        smooth_ite=var[price][-1]
    var['smooth_ite'].append(smooth_ite)


def SmoothITE_pandas(price,alpha,var):

    df=pd.DataFrame(var)

    df['smooth_ite']=np.nan
    df.loc[0,'smooth_ite']=df[price].iloc[0]
    avg_price=(df[price]+df[price].shift(1))/2 

    for i in range(1,df.shape[0]):
        df.loc[i,'smooth_ite']=alpha*avg_price.iloc[i]+(1-alpha)*df.loc[i-1,'smooth_ite']

    var['smooth_ite']=df['smooth_ite'].tolist()

    


