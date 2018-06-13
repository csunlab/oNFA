# -*- coding: utf-8 -*-
"""
Ahmad, N., Derrible, S., Managi, S., 2018, A network-based frequency analysis of Inclusive Wealth to track sustainable development in world countries, Journal of Environmental Management, 218:348-354,
https://doi.org/10.1016/j.jenvman.2018.04.070.
"""

import pandas as pd 
import os
import numpy as np
import matplotlib.pyplot as plt


def orbital_diagram(filename):

    mypath=os.path.join(os.getcwd(),'%s_Result'%(filename))
    
    #==============================================================================
    # Read the first year data 
    #==============================================================================
    
    df_orbit=pd.read_csv(os.path.join(mypath,
                                      '%s_optimum_%s.csv'%(filename,1990)),
    index_col='Cutoff_per')
                                                                       
    #print df_orbit.index
    
    end_point=list(df_orbit.index).index('Cluster analysis')
    
    #df_orbit=df_orbit.iloc[3:end_point]
    
    col=df_orbit.columns[:6]
    
    #print col
    df_orbit=df_orbit[col]
    header=df_orbit.iloc[3]
    #print header
    df_orbit=df_orbit.iloc[4:end_point]
    df_orbit.columns=header
    df_orbit=df_orbit[['Country','Rank']]
    df_orbit.columns=['Country','%s'%(1990)]
    #print df_orbit.head(),len(df_orbit.index)
    
    
    #==============================================================================
    # read the other years data and then merge it with the first year
    #==============================================================================
    for year in range(1991,2015):
    
        df_temp=pd.read_csv(os.path.join(mypath,
                '%s_optimum_%s.csv'%(filename,year)),
        index_col='Cutoff_per')
                                                                           
        #print df_orbit.index
        
        end_point=list(df_temp.index).index('Cluster analysis')
        
        #df_orbit=df_orbit.iloc[3:end_point]
        
        col=df_temp.columns[:6]
        
        #print col
        df_temp=df_temp[col]
        header=df_temp.iloc[3]
        #print header
        df_temp=df_temp.iloc[4:end_point]
        df_temp.columns=header
        df_temp=df_temp[['Country','Rank']]
        df_temp.columns=['Country','%s'%(year)]
        #print df_temp.head(), len(df_temp.index)
        
        df_orbit=pd.merge(df_orbit,df_temp,how='outer',on='Country')
    
    df_orbit.sort_values(by=['Country'],ascending=True,inplace=True)    
    df_orbit.to_csv(os.path.join(mypath,
    '%s_orbital_position.csv'%(filename)),
                    index=False)
    
    
    #==============================================================================
    # Create the rank clock for all the countries 
    #==============================================================================
    df_rank=pd.read_csv(os.path.join(mypath,
                '%s_orbital_position.csv'%(filename)),
    index_col='Country')
    
    
    
    theta=[2*np.pi*i/len(df_rank.columns) for i in range(1,
           len(df_rank.columns)+1)]
    
   
    
    
    fig=plt.figure(figsize=(36.4,15))
    
    for i in range(len(df_rank.index)):
        
        ax=fig.add_subplot(8,20,i+1,polar=True)
        ax.plot(theta,df_rank.iloc[i],color='#00e6e6')
        ax.set_thetagrids([360.0*j/25 for j in range(8,25,8)],
                           range(1990+7,2015,8),frac=1.2)
                           
        ax.set_ylim(0,300)
        #ax.grid(b='off',which='both',axis='y')
        
        plt.rgrids((100,200,300))
        ax.set_yticklabels([])
        ax.text(0.35,-0.15,
            df_rank.index[i],
                verticalalignment='center', horizontalalignment='center',
                transform=ax.transAxes,fontsize=12,color='black')
    
    
    fig.tight_layout()
    if filename=='HC':
        fig.text(0.5,0.07,'Orbital Diagrams for %s'%(filename),fontsize=30,
             horizontalalignment='center',color='#660000')
    elif filename=='NC':
        fig.text(0.5,0.07,'Orbital Diagrams for %s'%(filename),fontsize=30,
             horizontalalignment='center',color='#660000')
    elif filename=='PC':
        fig.text(0.5,0.07,'Orbital Diagrams for %s'%(filename),fontsize=30,
             horizontalalignment='center',color='#660000')
    fig.savefig('%s_Orbital_Diagram.png'%(filename))
    fig.savefig('%s_Orbital_Diagram.pdf'%(filename))
    plt.close('all')
    
#orbital_diagram('HC')
