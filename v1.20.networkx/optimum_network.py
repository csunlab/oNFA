# -*- coding: utf-8 -*-
"""
Ahmad, N., Derrible, S., Managi, S., 2018, A network-based frequency analysis of Inclusive Wealth to track sustainable development in world countries, Journal of Environmental Management, 218:348-354,
https://doi.org/10.1016/j.jenvman.2018.04.070.
"""


import csv
import networkx as nx
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
    
    g=nx.Graph() # create the graph using networkX
    
    value=list(df1['%s'%(year)])
    value=dict(zip(range(len(value)),value))
    
    country=list(df1['Country'])
    country=dict(zip(range(len(value)),country))
    
    g.add_nodes_from(range(len(value)))
    nx.set_node_attributes(g,value,'value') #store all the values as node attributes.
    nx.set_node_attributes(g,country,'country') #store name of all nodes attributes.
    
    
    df_co=pd.read_csv(os.path.join(mypath,
    '%s_parameters_%s.csv'%(filename,year)))
    
#    find the optimum cutoff for the optimum network, where five consecutive
#    cutoffs yield minimal/zero change in the size of the giant cluster and also
#    ensure a certain percentage (i.e., 60%) of nodes in the giant cluster

    df_co=df_co[df_co['stdev']==0 ]
    df_co=df_co[df_co['G_ratio']> 0.60] 
   
    cutoff_1=float(list(df_co.iloc[0])[1]) # get the optimum cutoff
    
    mode=float(list(df_co.iloc[0])[6]) # get the N mode
    mode_id=int(list(df_co.iloc[0])[7]) # get the ID of the N mode
    
    # create the edge list. Two nodes are connected when the
    #values are within the cutoff
    edge=[] 
    for i in range(len(value)):
        for k in range(len(value)):
            if (g.nodes[i]["value"]-cutoff_1)<=g.nodes[k]["value"]<=(g.nodes[i]["value"]+cutoff_1) and i!=k :
                edge.append((i,k))
    
    edge=list(set(tuple(sorted(t)) for t in edge))
    g.add_edges_from(edge) # add the edges to the graph
      
    c3=max(nx.connected_component_subgraphs(g), key=len) # get the giant cluster
    
    # find all the subgraphs and their properties in the graph
    com=[list(c.nodes) for c in list(nx.connected_component_subgraphs(g))]
    com_list=[]

    for i in range(len(value)):
        for j in range(len(com)):
            if i in com[j]:
                com_list.append((i,j))
                
    com_list=dict(com_list)
    nx.set_node_attributes(g,com_list,'cluster')
    
    # Store name, value, degree and orbital position of each node in the graph 
    final=[]
    for i in range(0,len(value)):
        
        try:
            if g.nodes[i]["value"]>mode:
                final.append([i,g.nodes[i]["country"],g.nodes[i]["value"],g.degree(i),
                              g.nodes[i]["cluster"],
        nx.shortest_path_length(g,source=mode_id,target=i),
        100+math.ceil((g.nodes[i]["value"]-mode)/cutoff_1)])
        
            else:
                final.append([i,g.nodes[i]["country"],g.nodes[i]["value"],g.degree(i),
                              g.nodes[i]["cluster"],
        nx.shortest_path_length(g,source=mode_id,target=i),
        100+math.floor((g.nodes[i]["value"]-mode)/cutoff_1)])
                
            final=sorted(final,key=itemgetter(2),reverse=True)                
            df_optimum=pd.DataFrame(final)
            df_optimum.columns=['ID','Country','Value','Degree',
            'cluster','sht','Rank']
        except:
            if g.nodes[i]["value"]>mode:
                final.append([i,g.nodes[i]["country"],g.nodes[i]["value"],g.degree(i),
                              g.nodes[i]["cluster"],
        'inf',
        100+math.ceil((g.nodes[i]["value"]-mode)/cutoff_1)])
        
            else:
                final.append([i,g.nodes[i]["country"],g.nodes[i]["value"],g.degree(i),
                              g.nodes[i]["cluster"],
        'inf',
        100+math.floor((g.nodes[i]["value"]-mode)/cutoff_1)])
                
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
        new.writerow(['edge',nx.number_of_edges(g)])
        new.writerow(['Giant_cluster',g.nodes[mode_id]["cluster"],
                      'size',nx.number_of_nodes(c3)])
                      
        
        new.writerow(['ID','Country','Value','Degree',
        'cluster','sht','Rank'])
    
        for row in final:
            new.writerow(row)
        
        new.writerow(['Cluster analysis'])
        for i in range(len(com)):
        
            new.writerow([i,[g.nodes[j]["country"] for j in com[i]],
                            len(com[i])])
            
        out.close()
    except:
        out=open(os.path.join(mypath,
        '%s_optimum_%s.csv'%(filename,year)),'w')
        new=csv.writer(out)
        new.writerow(df_co.columns)
        new.writerow(df_co.iloc[0])
        new.writerow(['edge',nx.number_of_edges(g)])
        new.writerow(['Giant_cluster',g.nodes[mode_id]["cluster"],
                      'size',nx.number_of_nodes(c3)])
                      
        
        new.writerow(['ID','Country','Value','Degree',
        'cluster','sht','Rank'])
    
        for row in final:
            new.writerow(row)
        
        new.writerow(['Cluster analysis'])
        for i in range(len(com)):
        
            new.writerow([i,[g.nodes[j]["country"] for j in com[i]],
                            len(com[i])])
            
        out.close()
# plot the degree distribution 
    plt.plot(df_optimum['Value'],df_optimum['Degree'])
    
    plt.xscale('log') # transform the x axis to log scale
    plt.xlim(xmin=1000)
    plt.ylim(0,50)
    plt.annotate('Year-%s\nCutoff-%.2f\nMode-%.2f\nCountry-%s\nH_index-%.2f'%(year,cutoff_1,mode,
list(df_co.iloc[0])[5],float(list(df_co.iloc[0])[-2])),xy=(0.97, 0.96), 
xycoords='axes fraction', fontsize=12,
                horizontalalignment='right', verticalalignment='top')
    plt.savefig(os.path.join(mypath,'%s_optimum_%s.pdf'%(filename,year)))
    plt.savefig(os.path.join(mypath,'%s_optimum_%s.png'%(filename,year)))
    plt.close('all')
