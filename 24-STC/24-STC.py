import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
import numpy as np
import pandas as pd
import random
import indicator as indi

class STC:
    def __init__(self):
        self.n=200
        self.fig=plt.figure()
        self.title='STC'
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

            #STC:
            if self.calc_type=='dict':
                self.indi.stc_dict(23,50,10,3,var)

            self.print_data(var)
        
        if self.calc_type=='pandas':
            self.indi.stc_pandas(23,50,10,3,var)

    def plot_data(self,var):
        self.fig.subplots_adjust(top=0.95,bottom=0.05,right=0.98,left=0.1,hspace=0,wspace=0)
        ax=self.fig.add_gridspec(6,1)
        ax1=self.fig.add_subplot(ax[0:5,:])
        ax2=self.fig.add_subplot(ax[5:6,:])

        ax1.clear()
        ax1.set_xticks([])
        ax1.set_title(self.title)
        fr=100

        for i in range(len(var['time'][-fr:])):
            if var['open'][-fr:][i]>var['close'][-fr:][i]:
                ccolor='r'
            elif var['open'][-fr:][i]<var['close'][-fr:][i]:
                ccolor='g'
            else:
                ccolor='gray'
            ax1.plot([var['time'][-fr:][i]]*2,[var['open'][-fr:][i],var['close'][-fr:][i]],c=ccolor,lw=3)
            ax1.plot([var['time'][-fr:][i]]*2,[var['high'][-fr:][i],var['low'][-fr:][i]],c=ccolor,lw=0.5)

        #plot STC:
        ax2.clear()
        ax2.set_xticks([])
        ax2.set_ylim(0,100)
        for i in [20,80]:
            ax2.axhline(y=i,c='dimgray',lw=1,ls='--')

        #'''
        for i in range(len(var['time'][-fr:])):
            if i>=1:
                if var['dd_macd'][-fr:][i]>var['dd_macd'][-fr:][i-1]:
                    ccolor='g'
                elif var['dd_macd'][-fr:][i]<var['dd_macd'][-fr:][i-1]:
                    ccolor='r'
                else:
                    ccolor='gray'
                ax2.plot([var['time'][-fr:][i-1],var['time'][-fr:][i]],[var['dd_macd'][-fr:][i-1],var['dd_macd'][-fr:][i]],c=ccolor,lw=1)
        #'''

        plt.show()


obj=STC()
var=obj.set_variables()
obj.get_data(var)
obj.plot_data(var)




