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
import datetime
import seaborn


Time=datetime.datetime.now()
try:
    f_name=raw_input('enter filename-') # enter filename for python 2
  
except:
    f_name=input('enter filename-')# enter filename for python 3
    
    
df_main=pd.read_csv('%s.csv'%(f_name)) # read the data file
start_yr=int(df_main.columns[1])
end_yr=int(df_main.columns[-1])+1

print ('Analyzing %s'%(f_name))

import network
network.network_complete(f_name) # run the network.py 

import optimum_network # find the optimum network and store results of the optimum network
for year in range(start_yr,end_yr,1):
    optimum_network.network_optimum(f_name,year)
    
import orbital # generate orbital digrams
orbital.orbital_diagram(f_name)

import orbital_speed # compute orbital speeds
orbital_speed.orbital_speed(f_name)

print ('Finished Analyzing %s'%(f_name))

print ('Total time taken-%s'%(datetime.datetime.now()-Time))
