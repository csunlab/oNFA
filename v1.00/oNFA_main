# -*- coding: utf-8 -*-
"""
Ahmad, N., Derrible, S., Managi, S., 2018, A network-based frequency analysis of
Inclusive Wealth to track sustainable development in world countries,
Journal of Environmental Management, 218:348-354,
https://doi.org/10.1016/j.jenvman.2018.04.070.
"""

import csv
from igraph import*
import pandas as pd
import numpy as np
import os
import datetime
import seaborn

Time=datetime.datetime.now()
files=['HC','NC','PC']
#f_name=raw_input('enter filename-')

for f_name in files:
    
    print ('Analyzing %s'%(f_name))
    import network
    
    network.network_complete(f_name)
    
    import optimum_network
    for year in range(1990,2015,1):
        optimum_network.network_optimum(f_name,year)
        
    import orbital
    
    orbital.orbital_diagram(f_name)
    
    import orbital_speed
    
    orbital_speed.orbital_speed(f_name)
    
    print ('Finished Analyzing %s'%(f_name))
import o_speed_vis
o_speed_vis.o_speed_vis()


print 'Total time taken-',datetime.datetime.now()-Time
