import matplotlib.pyplot as plt
from datetime import datetime,timedelta
import numpy as np
import pandas as pd
import random
import indicator as indi

class EMA:
    def __init__(self):
        self.n=100
        self.fig=plt.figure()
        self.title='EMA'
        self.calc_type='pandas'   #'dict' or 'pandas'
        self.indi=indi

    def set_variables(self):
        variables=['time','open','high','low','close']
        var={i:[] for i in variables}
        return var

    def print_data(self,var):
        print(var['time'][-1],f"O:{var['open'][-1]:.5f}",f"H:{var['high'][-1]:.5f}"
              f"L:{var['low'][-1]:.5f}",f"C:{var['close'][-1]:.5f}")

    def get_data(self,var):
        for i in range(self.n):
            t=(datetime.now()+timedelta(minutes=i)).strftime('%d-%m-%Y %H:%M:%S')
            var['time'].append(t)

            if len(var['open'])==0:
                var['open'].append(random.uniform(1,1.2))
                up_close=var['open'][-1]*(1+0.0001)
                down_close=var['open'][-1]*(1-0.0001)
                var['close'].append(random.uniform(down_close,up_close))
            else:
                var['open'].append(var['close'][-1])
                up_close=var['open'][-1]*(1+0.0001)
                down_close=var['open'][-1]*(1-0.0001)
                var['close'].append(random.uniform(down_close,up_close))
        
            if var['open'][-1]<var['close'][-1]:
                price1=var['close'][-1]
                price2=var['open'][-1]
            elif var['open'][-1]>var['close'][-1]:
                price1=var['open'][-1]
                price2=var['close'][-1]
            high=random.uniform(price1,price1*(1+0.00007))
            low=random.uniform(price2,price2*(1-0.00007))
            var['high'].append(high)
            var['low'].append(low)

            #SMMA:
            if self.calc_type=='dict':
                n_list=[20,50]
                for n in n_list:
                    self.indi.ema_dict(n,'close',var)

            self.print_data(var)

        if self.calc_type=='pandas':
            n_list=[20,50]
            for n in n_list:
                var[f'ema{n}']=self.indi.ema_pandas(n,'close',var)

    def plot_data(self,var):
        self.fig.subplots_adjust(top=0.95,bottom=0.05,right=0.98,left=0.1,hspace=0,wspace=0)
        ax=self.fig.add_subplot()

        ax.clear()
        ax.set_title(self.title)
        ax.set_xticks(np.arange(0,len(var['time']),40))

        for i in range(len(var['time'])):
            if var['open'][i]>var['close'][i]:
                ccolor='r'
            elif var['open'][i]<var['close'][i]:
                ccolor='g'
            else:
                ccolor='gray'
            ax.plot([var['time'][i]]*2,[var['open'][i],var['close'][i]],c=ccolor,lw=3)
            ax.plot([var['time'][i]]*2,[var['high'][i],var['low'][i]],c=ccolor,lw=0.5)

        #PLOT SMMA:
        ema_keys=[k for k in var.keys() if 'ema' in k]
        if len(ema_keys)>=1:
            for ema in ema_keys:
                ax.plot(var['time'],var[ema],lw=1.5,label=ema)
            ax.legend()

        plt.show()

obj=EMA()
var=obj.set_variables()
obj.get_data(var)
obj.plot_data(var)




