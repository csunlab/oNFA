# -*- coding: utf-8 -*-
"""
Ahmad, Derrible, Managi. A Network-Based Frequency Approach to 
Representing the Inclusive Wealth of World Countries.

"""
import os 
import pandas as pd 





def max_o_pos(filename):
    year=1990
    #i=0    
    mypath=os.getcwd()+'\%s_Result'%(filename)
    
    
    df=pd.read_csv(os.path.join(mypath,
    '%s_optimum_%s.csv'%(filename,year)),index_col='Cutoff_per')
    
    
    
    giant_cluster=int(df.loc['Giant_cluster'][0])
    
    #print giant_cluster
    
    end_point=list(df.index).index('Cluster analysis')
    
    #print end_point
    
    col=df.columns[:6]
        
        #print col
    df=df[col]
    header=df.iloc[3]
    #print header
    df=df.iloc[4:end_point]
    df.columns=header
    df=df[['Country','cluster','Rank']]
    df['Rank']=df['Rank'].astype(float)
    #print df.head(),len(df.index),max(df['Rank'])
    df=df[df['cluster']==str(giant_cluster)]
    
    df_final=df[['Country','Rank']]
    
    df_final.columns=['Country','%s_%s'%(filename,year)]
    
    
    
    max_list=[]
    
    for year in range(1991,2015,1):
        
        mypath=os.getcwd()+'\%s_Result'%(filename)
    
    
        df=pd.read_csv(os.path.join(mypath,
        '%s_optimum_%s.csv'%(filename,year)),index_col='Cutoff_per')
        
        
        
        giant_cluster=int(df.loc['Giant_cluster'][0])
        
        #print giant_cluster
        
        end_point=list(df.index).index('Cluster analysis')
        
        #print end_point
        
        col=df.columns[:6]
            
            #print col
        df=df[col]
        header=df.iloc[3]
        #print header
        df=df.iloc[4:end_point]
        df.columns=header
        df=df[['Country','cluster','Rank']]
        df['Rank']=df['Rank'].astype(float)
        #print df.head(),len(df.index),max(df['Rank'])
        df=df[df['cluster']==str(giant_cluster)]
        
        df1=df[['Country','Rank']]
        #print filename,year,max(df1['Rank'])
        max_list.append(max(df1['Rank']))
        df1.columns=['Country','%s_%s'%(filename,year)]
        df_final=pd.merge(df_final,df1,on='Country',how='outer')
        
        
    df_final=df_final.set_index('Country')
    df_final.to_csv('%s_o-pos-giantcountry.csv'%(filename))
    #pd.DataFrame.set_index()
    #print df_final.dtypes  
    #print df_final.head(),len(df_final.index)
    
    
    return filename,max_list,max(max_list)


def final_o_pos():
    files=['HC','NC','PC']
    max_op=[]
    
    for file1 in files:
        max_op.append(max_o_pos(file1)[-1])
        
    return max_op
