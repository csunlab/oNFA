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


def network_optimum(filename,year):
    
    df=pd.read_csv('%s.csv'%(filename)) # read the csv file using pandas
    df=df.replace(np.NaN,-5,regex=True) # take care of the empty cells
    
    
    mypath=os.path.join(os.getcwd(),'%s_Result'%(filename)) # Access the folder path, where, all results are stored
    
  
    df1=df[['Country','%s'%(year)]]
    df1=df1[df1['%s'%(year)]!=-5]
    
    g=Graph() # create the graph using igraph
    
    value=list(df1['%s'%(year)])
    country=list(df1['Country'])
    
    g.add_vertices(len(value))
    g.vs["value"]=value  #store all the values as node attributes.
    
    
    df_co=pd.read_csv(os.path.join(mypath,
    '%s_parameters_%s.csv'%(filename,year)))
    df_co=df_co[df_co['stdev']==0 ]

#    find the optimum cutoff for the optimum network, where five consecutive
#    cutoffs yield minimal/zero change in the size of the giant cluster and also
#    ensure a certain percentage (i.e., 60%) of nodes in the giant cluster

    df_co=df_co[df_co['G_ratio']> 0.60]        
    cutoff_1=float(list(df_co.iloc[0])[1]) # get the optimum cutoff
    
    mode=float(list(df_co.iloc[0])[6]) # get the N mode
    mode_id=int(list(df_co.iloc[0])[7]) # get the ID of the N mode
     
    # create the edge list. Two nodes are connected when the
    #values are within the cutoff
    edge=[]
    for i in range(len(value)):
        for k in range(len(value)):
            if (g.vs["value"][i]-cutoff_1)<=g.vs["value"][k]<=(g.vs["value"][i]+cutoff_1) and i!=k :
                edge.append((i,k))
    g.add_edges(edge) # add the edges to the graph
    g.simplify(multiple=True,loops=True,combine_edges=None)
    
    c1=g.clusters(2)
    c3=c1.giant() # get the giant cluster
    
 # Store name, value, degree and orbital position of each node in the graph
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
    
# Store all results in a csv file

    try:
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
    except:
        out=open(os.path.join(mypath,
        '%s_optimum_%s.csv'%(filename,year)),'w')
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
        
# plot the degree distribution 
    
    plt.plot(df_optimum['Value'],df_optimum['Degree'])
    plt.xscale('log')  # transform the x axis to log scale
    plt.xlim(xmin=1000)
    plt.ylim(0,50)
    plt.annotate('Year-%s\nCutoff-%.2f\nMode-%.2f\nCountry-%s\nH_index-%.2f'%(year,cutoff_1,mode,
list(df_co.iloc[0])[5],float(list(df_co.iloc[0])[-2])),xy=(0.97, 0.96), 
xycoords='axes fraction', fontsize=12,
                horizontalalignment='right', verticalalignment='top')
    plt.savefig(os.path.join(mypath,'%s_optimum_%s.pdf'%(filename,year)))
    plt.savefig(os.path.join(mypath,'%s_optimum_%s.png'%(filename,year)))
    plt.close('all')
