# -*- coding: utf-8 -*-
"""
Ahmad, N., Derrible, S., Managi, S., 2018, A network-based frequency analysis of Inclusive Wealth to track sustainable development in world countries, Journal of Environmental Management, 218:348-354,
https://doi.org/10.1016/j.jenvman.2018.04.070.
"""


import networkx as nx
import pandas as pd
import numpy as np
import os


def network_complete(filename):

    df=pd.read_csv('%s.csv'%(filename))# read the csv file using pandas
    df=df.replace(np.NaN,-5,regex=True) # take care of the empty cells
    
    def network(year,cutoff): # create a function to generate the network
        df1=df[['Country','%s'%(year)]]
        df1=df1[df1['%s'%(year)]!=-5]
        
        g=nx.Graph() # create the graph using networkX
        
        value=list(df1['%s'%(year)])
        value=dict(zip(range(len(value)),value))
        
        country=list(df1['Country'])
        country=dict(zip(range(len(value)),country))
        
        g.add_nodes_from(range(len(value)))
        nx.set_node_attributes(g,value,'value') #store all the values as node attributes.
        nx.set_node_attributes(g,country,'country')  #store name of all nodes attributes.
        
        # compute cutoof as a percentage of the median
        cutoff_1=np.median(list(value.values()))*float(cutoff)/100.0
        
        # create the edge list. Two nodes are connected when the
    #values are within the cutoff
        edge=[]
        for i in range(len(value)):
            for k in range(len(value)):
                if (g.nodes[i]["value"]-cutoff_1)<=g.nodes[k]["value"]<=(g.nodes[i]["value"]+cutoff_1) and i!=k :
                    edge.append((i,k))
        
        edge=list(set(tuple(sorted(t)) for t in edge))
        
        g.add_edges_from(edge) # add the edges to the graph     
        c3=max(nx.connected_component_subgraphs(g), key=len)  # get the giant cluster
        
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
            final.append([i,g.nodes[i]["country"],g.nodes[i]["value"],g.degree(i),
                          g.nodes[i]["cluster"]])
        
        df2=pd.DataFrame(final).sort_values(by=[2],ascending=False)
        df2.columns=['ID','Country','Value','Degree','cluster']
          
        df_mode=df2[df2['Degree']==max(df2['Degree'])]
        df_mode_1=list(df_mode.iloc[-1])
        
        # return all parameters for each generated network
        return [cutoff,cutoff_1,g.number_of_nodes(),nx.diameter(c3), nx.density(g),df_mode_1[1],
                df_mode_1[2],df_mode_1[0],nx.average_shortest_path_length(c3),nx.density(c3), 
        float(c3.number_of_nodes())/g.number_of_nodes(),float(cutoff_1)/float(df_mode_1[2])]  


    os.mkdir('%s_Result'%(filename)) # create a folder to store results
   
    mypath=os.path.join(os.getcwd(),'%s_Result'%(filename))
    for year in range(1990,2015,1):
        
        print ('starting %s'%(year))
        parameters=[]
        
        # generate 100 networks for each column using cutodd from 1% of 
        # the median to 100% of the median
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
        
        # save all parameters for 100 netwroks for each column in a csv file
        df_param.to_csv(os.path.join(mypath,
        '%s_parameters_%s.csv'%(filename,year)),index=False)
