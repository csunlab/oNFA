# -*- coding: utf-8 -*-
"""
Ahmad, N., Derrible, S., Managi, S., 2018, A network-based frequency analysis of Inclusive Wealth to track sustainable development in world countries, Journal of Environmental Management, 218:348-354,
https://doi.org/10.1016/j.jenvman.2018.04.070.
"""

import csv
from igraph import*
import pandas as pd
import numpy as np
import os
import datetime

Time=datetime.datetime.now()

def network_complete(filename):

    df=pd.read_csv('%s.csv'%(filename))
    df=df.replace(np.NaN,-5,regex=True)
    
    def network(year,cutoff):
        df1=df[['Country','%s'%(year)]]
        df1=df1[df1['%s'%(year)]!=-5]
        
        #print df1.head(),len(df1.index)
       
        g=Graph()
        
        value=list(df1['%s'%(year)])
        country=list(df1['Country'])

        g.add_vertices(len(value))
        g.vs["value"]=value
        
        #print g.vs["value"]
        
        
        #print summary(g)
        #        
        #        
        #        
        cutoff_1=np.median(value)*float(cutoff)/100.0
        
        #print 'Cutoff-',cutoff_1
        #
        #
        #
        edge=[]
        for i in range(len(value)):
            for k in range(len(value)):
                if (g.vs["value"][i]-cutoff_1)<=g.vs["value"][k]<=(g.vs["value"][i]+cutoff_1) and i!=k :
                    edge.append((i,k))
        #print edge
        g.add_edges(edge)
        g.simplify(multiple=True,loops=True,combine_edges=None)
        #print g.get_edgelist()
        #print summary(g)
        
        #return [cutoff,cutoff_1,diame]
        c1=g.clusters(2)
    
        #print summary(c1)
        
        c3=c1.giant()
        final=[]
        for i in range(0,len(value)):
            final.append([i,country[i],g.vs["value"][i],g.degree(i),
                          c1.membership[i]])
        #df2=pd.DataFrame(final).sort_values(columns=2,ascending=False)
        df2=pd.DataFrame(final).sort_values(by=[2],ascending=False)
      
        #print df2.head()
        
        
        df2.columns=['ID','Country','Value','Degree','cluster']
        
        #df2.to_csv('test.csv',index=False)
        df_mode=df2[df2['Degree']==max(df2['Degree'])]
        df_mode_1=list(df_mode.iloc[-1])
        return [cutoff,cutoff_1,g.vcount(),g.diameter(), g.density(),df_mode_1[1],
                df_mode_1[2],df_mode_1[0],g.average_path_length(),c3.density(), 
    float(c3.vcount())/g.vcount(),float(cutoff_1)/float(df_mode_1[2])]
    
    os.mkdir('%s_Result'%(filename))
    
    #mypath=os.getcwd()+'\%s_Result'%(filename)
    mypath=os.path.join(os.getcwd(),'%s_Result'%(filename))
    for year in range(1990,2015,1):
        
        print ('starting %s'%(year))
        parameters=[]
        for cutoff in range(1,101):
            
            parameters.append(network(year,cutoff))
            
        df_param=pd.DataFrame(parameters)
        
        df_param.columns=['Cutoff_per','Cutoff','Nodes','Dia','Density',
                  'Country','Mode','Mode_ID','Avg_shtst','G_density','G_ratio',
                  'H_index']
        stdev_list=[]
        for i in range(len(df_param['G_ratio'])-5):
            
            stdev_list.append('%0.2f'%(np.std(df_param['G_ratio'].iloc[i:i+5],
                                              ddof=1)))
        stdev_list.extend([0]*(len(df_param['G_ratio'])-len(stdev_list)))                                      
        df_param['stdev']=stdev_list
                                              
        
    
        df_param.to_csv(os.path.join(mypath,
        '%s_parameters_%s.csv'%(filename,year)),index=False)

#print 'Total time taken-',datetime.datetime.now()-Time
