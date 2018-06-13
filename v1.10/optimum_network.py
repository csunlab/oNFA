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
import math
from operator import itemgetter
import matplotlib.pyplot as plt
import time


def network_optimum(filename,year):
    
    df=pd.read_csv('%s.csv'%(filename))
    df=df.replace(np.NaN,-5,regex=True)

    mypath=os.path.join(os.getcwd(),'%s_Result'%(filename))
    
    #print mypath
    df1=df[['Country','%s'%(year)]]

    df1=df1[df1['%s'%(year)]!=-5]
    
    #print df1.head(),len(df1.index)
    
    
    g=Graph()
    
    value=list(df1['%s'%(year)])
    country=list(df1['Country'])
    
    g.add_vertices(len(value))
    g.vs["value"]=value
    
    df_co=pd.read_csv(os.path.join(mypath,
    '%s_parameters_%s.csv'%(filename,year)))
    df_co=df_co[df_co['stdev']==0 ]

    df_co=df_co[df_co['G_ratio']> 0.60]        
    cutoff_1=float(list(df_co.iloc[0])[1])
    
    mode=float(list(df_co.iloc[0])[6])
    mode_id=int(list(df_co.iloc[0])[7])
    #print (cutoff_1,mode,mode_id)
    
    
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
        if g.vs["value"][i]>mode:
            final.append([i,country[i],g.vs["value"][i],g.degree(i),
                          c1.membership[i],
    g.shortest_paths(mode_id,i)[0][0],
    100+math.ceil((g.vs["value"][i]-mode)/cutoff_1)])
    
        else:
            final.append([i,country[i],g.vs["value"][i],g.degree(i),
                          c1.membership[i],
    g.shortest_paths(mode_id,i)[0][0],
    100+math.floor((g.vs["value"][i]-mode)/cutoff_1)])
            
    final=sorted(final,key=itemgetter(2),reverse=True)                
    df_optimum=pd.DataFrame(final)
    
    df_optimum.columns=['ID','Country','Value','Degree',
    'cluster','sht','Rank']
#    
#    df_optimum.to_csv('test_optimum.csv',index=False)
    
    out=open(os.path.join(mypath,
    '%s_optimum_%s.csv'%(filename,year)),'wb')
    new=csv.writer(out)
    new.writerow(df_co.columns)
    new.writerow(df_co.iloc[0])
    new.writerow(['edge',g.ecount()])
    new.writerow(['Giant_cluster',c1.membership[mode_id],
                  'size',c3.vcount()])                 
    
    new.writerow(['ID','Country','Value','Degree',
    'cluster','sht','Rank'])

    for row in final:
        new.writerow(row)
    
    new.writerow(['Cluster analysis'])
    for i in range(len(c1)):
    
        new.writerow([i,[country[j] for j in c1[i]],
                        len([country[j] for j in c1[i]])])
        
    out.close()

    plt.plot(df_optimum['Value'],df_optimum['Degree'])
    
    plt.xscale('log')
    plt.xlim(xmin=1000)
    plt.ylim(0,40)
    plt.annotate('Year-%s\nCutoff-%.2f\nMode-%.2f\nCountry-%s\nH_index-%.2f'%(year,cutoff_1,mode,
list(df_co.iloc[0])[5],float(list(df_co.iloc[0])[-2])),xy=(0.97, 0.96), 
xycoords='axes fraction', fontsize=12,
                horizontalalignment='right', verticalalignment='top')
    plt.savefig(os.path.join(mypath,'%s_optimum_%s.pdf'%(filename,year)))
    plt.savefig(os.path.join(mypath,'%s_optimum_%s.png'%(filename,year)))
    plt.close('all')
    #plt.suptitle()
    
    #plt.annotate()
