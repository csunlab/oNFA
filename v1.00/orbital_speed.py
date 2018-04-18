# -*- coding: utf-8 -*-
"""
Ahmad, Derrible, Managi. A Network-Based Frequency Approach to 
Representing the Inclusive Wealth of World Countries.
"""


import os 
import pandas as pd
import numpy as np 



def orbital_speed(filename):
    mypath=os.getcwd()+'\%s_Result'%(filename)
    
    
    df=pd.read_csv(os.path.join(mypath,
    '%s_orbital_position.csv'%(filename)),index_col='Country')
    
    #print df.head()
    df1=pd.read_csv(os.path.join(mypath,
    '%s_orbital_position.csv'%(filename)),index_col='Country')
    df1=df1.replace(np.nan,-5,regex=True)
    def o_speed(x):
        
        x_sum=0
        
        for i in range(1,len(x)):
            
            if x[i]!=-5 and x[i-1]!=-5:
            
                x_sum+= x[i]-x[i-1]
            
        return x_sum
        
    
    df1['speed_total']=df1.apply(o_speed,axis=1)
    
    df1['avg_speed']=float(0)
    for i in range(len(df1.index)):
    #    print float(df1['speed_total'][i])
    #    print df.iloc[i].count()
        df1['avg_speed'][i]='%.2f'%(float(df1['speed_total'][i])/float(df.iloc[i].count()-1))
    
    
    
    df1.to_csv(os.path.join(mypath,'%s_Orbital_Speed.csv'%(filename)))
    
    
#orbital_speed('HC')
