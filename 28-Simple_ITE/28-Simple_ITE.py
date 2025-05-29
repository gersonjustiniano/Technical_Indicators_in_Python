import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
import numpy as np
import pandas as pd
import random
import indicator as indi

class Simple_ITE:
    def __init__(self):
        self.n=100
        self.fig=plt.figure()
        self.title='Simple Instantaneous Trendline Ehlers'
        self.calc_type='pandas'   #'dict' or 'pandas'
        self.indi=indi

    def set_variables(self):
        variables=['time','open','high','low','close']
        var={i:[] for i in variables}
        return var

    def print_data(self,var):
        print(len(var['time']),var['time'][-1],f"O:{var['open'][-1]:.5f}",f"H:{var['high'][-1]:.5f}"
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

            #Simple ITE:
            if self.calc_type=='dict':
                self.indi.SimpleITE_dict('close',var)

            self.print_data(var)
        
        if self.calc_type=='pandas':
            self.indi.SimpleITE_pandas('close',var)

    def plot_data(self,var):
        self.fig.subplots_adjust(top=0.95,bottom=0.05,right=0.98,left=0.1,hspace=0,wspace=0)
        ax=self.fig.add_gridspec(6,1)
        ax1=self.fig.add_subplot(ax[:,:])

        ax1.clear()
        ax1.set_xticks([])
        ax1.set_title(self.title)
        fr=100

        for i in range(len(var['time'][-fr:])):
            if var['open'][-fr:][i]>var['close'][-fr:][i]:
                ccolor='black'
            elif var['open'][-fr:][i]<var['close'][-fr:][i]:
                ccolor='gray'
            else:
                ccolor='gray'
            ax1.plot([var['time'][-fr:][i]]*2,[var['open'][-fr:][i],var['close'][-fr:][i]],c=ccolor,lw=3)
            ax1.plot([var['time'][-fr:][i]]*2,[var['high'][-fr:][i],var['low'][-fr:][i]],c=ccolor,lw=0.5)

        #plot Simple ITE:
        ax1.plot(var['time'],var['simple_ite'],c='r',lw=2)

        plt.show()

obj=Simple_ITE()
var=obj.set_variables()
obj.get_data(var)
obj.plot_data(var)




