import matplotlib.pyplot as plt
from datetime import datetime,timedelta
import numpy as np
import pandas as pd
import random
import indicator as indi

class Bollinger:
    def __init__(self):
        self.n=100
        self.fig=plt.figure()
        self.title='Bollinger Bands'
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

            #Bollinger:
            if self.calc_type=='dict':
                self.indi.bollinger_dict(20,2,'close',var)

            self.print_data(var)

        if self.calc_type=='pandas':
            self.indi.bollinger_pandas(20,2,'close',var)

    def plot_data(self,var):
        self.fig.subplots_adjust(top=0.95,bottom=0.05,right=0.98,left=0.1,hspace=0,wspace=0)
        ax=self.fig.add_gridspec(6,1)
        ax1=self.fig.add_subplot(ax[0:4,:])
        ax2=self.fig.add_subplot(ax[4:5,:])
        ax3=self.fig.add_subplot(ax[5:6,:])

        ax1.clear()
        ax1.set_title(self.title)
        ax1.set_xticks([])
        ax1.set_xlim(-1,len(var['time'])+1)

        for i in range(len(var['time'])):
            if var['open'][i]>var['close'][i]:
                ccolor='r'
            elif var['open'][i]<var['close'][i]:
                ccolor='g'
            else:
                ccolor='gray'
            ax1.plot([var['time'][i]]*2,[var['open'][i],var['close'][i]],c=ccolor,lw=3)
            ax1.plot([var['time'][i]]*2,[var['high'][i],var['low'][i]],c=ccolor,lw=0.5)

        #PLOT Bollinger:
        ax1.plot(var['time'],var['avg_BB'],c='black',lw=1)
        ax1.plot(var['time'],var['up_BB'],c='black',lw=1,label='Bollinger')
        ax1.plot(var['time'],var['down_BB'],c='black',lw=1)
        ax1.legend(loc='upper left')

        ax2.clear()
        ax2.set_xticks([])
        ax2.set_yticks([0,1])
        ax2.set_xlim(-1,len(var['time'])+1)
        [ax2.axhline(y=i,c='black',lw=0.7,ls='--') for i in [0,1]]
        ax2.plot(var['time'],var['percentB'],c='b',lw=1,label='Percent B%')
        ax2.legend(loc='upper left')

        ax3.clear()
        ax3.set_xticks(np.arange(0,len(var['time']),40))
        ax3.set_yticks([])
        ax3.set_xlim(-1,len(var['time'])+1)
        ax3.plot(var['time'],var['bandWidth'],c='b',lw=1,label='BandWidth')
        ax3.legend(loc='upper left')

        plt.show()

obj=Bollinger()
var=obj.set_variables()
obj.get_data(var)
obj.plot_data(var)




