# -*- coding: utf-8 -*-
"""
Ahmad, Derrible, Managi. A Network-Based Frequency Approach to 
Representing the Inclusive Wealth of World Countries.
"""
import pandas as pd 
import os
import matplotlib.pyplot as plt

def o_speed_vis():
    s_point=1
    files=['HC','NC','PC']
    
    mypath=os.getcwd()+'\%s_Result'%(files[0])
        
        
    df=pd.read_csv(os.path.join(mypath,
    '%s_Orbital_Speed.csv'%(files[0])))
    #print df.head()
    df_ospeed=df[['Country','avg_speed']]
    
    df_ospeed.columns=['Country','%s'%(files[0])]
    for i in range(1,3):
        mypath=os.getcwd()+'\%s_Result'%(files[i])
        df1=pd.read_csv(os.path.join(mypath,
        '%s_Orbital_Speed.csv'%(files[i])))
        
        df1=df1[['Country','avg_speed']]
    
        df1.columns=['Country','%s'%(files[i])]
        
        df_ospeed=pd.merge(df_ospeed,df1,how='outer',on='Country')
    
   
    
    df_ospeed.to_csv('Orbital-speed.csv',index=False)
    
    fig=plt.figure(figsize=(60,14))
    
    for i in range(len(df_ospeed.index)):
            
            ax=fig.add_subplot(8,20,i+1)
            
            #ax.bar([0.5,1.5,2.5],df_ospeed.iloc[i][1:4])
            speed_list=list(df_ospeed.iloc[i][s_point:s_point+3])
            speed_tick=[0.5,1.5,2.5]
            for j in range(3):
                
                if -0.5<=speed_list[j]<=0.5:
                    ax.bar(speed_tick[j],speed_list[j],color='#ffa64d')
                elif speed_list[j]>0.5:
                    ax.bar(speed_tick[j],speed_list[j],color='#333399')
                    
                elif speed_list[j]<0.5:
                    ax.bar(speed_tick[j],speed_list[j],color='#990000')
                
                    
            
            ax.set_ylim(-0.5,0.5)
            
            ax.hlines(0,0,4)
            plt.xticks([1,2,3],['HC','NC','PC'],rotation=45)
            ax.text(0.98,0.98,
                df_ospeed.iloc[i][0],
                    verticalalignment='top', horizontalalignment='right',
                    transform=ax.transAxes,fontsize=12,color='black')
            
            
            
    fig.tight_layout()
   
    fig.text(0.5,0.05,'Orbital Speed',
                 horizontalalignment='center',
                 fontsize=40,color='#660000')
    
    fig.savefig('orbital_speed.pdf')
    fig.savefig('orbital_speed.png')      


#o_speed_vis(4,00)
