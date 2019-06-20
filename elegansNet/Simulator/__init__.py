#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 17:33:34 2019

@author: jescab01
"""

def standardInit():
    from _simulation_ import simulation, representation
    ### Define simulation variables
    timesteps = 10
    sim_no = 1
    Psens=0.15   # Parameter for sensory neurons being excited by environment
    
    att=0.7     ## attenuatipon coefficient
    
    ratioRandomInit=0.2  # ratio of active nodes from random function (e.g. if random() < 0.2 --> activate node).
    c=0.2 # free parameter influence of weights [exin*(100*c)*weight]
    ##### Sensor stimulation parameters. (Go to data/sensoryNeuronTable1.jpg to choose rational combinations)
    area=[] ## Area: 'head', 'body', 'tail'. 
    LRb=[] ## LRb: 'L' (left), 'R' (right), 'b' (body).
    sensor=[] ## Sensor: 'oxygen', 'mechanosensor', 'propioSomatic', 'propioTail', 'propioPharynx',
             ## 'propioHead', 'chemosensor', 'osmoceptor', 'nociceptor', 'thermosensor', 'thermonociceptive'. 
    
    G, masterInfo, simInitActivity,  pathLength, hpTest, envActivation = simulation(timesteps, sim_no, ratioRandomInit, c, area, LRb, sensor, Psens, att)
    representation(G, masterInfo, sim_no, timesteps, simInitActivity)
    return masterInfo, simInitActivity, pathLength, envActivation


def activityInit():
    
    from _simulation_ import simulation, representation
    ### Define simulation variables
    timesteps = 50
    sim_no = 1
    Psens=0.5   # Parameter for sensory neurons being excited by environment
    
    att=0.55     ## attenuatipon coefficient
    
    ratioRandomInit=0.5  # ratio of active nodes from random function (e.g. if random() < 0.2 --> activate node).
    c=0.2 # free parameter influence of weights [exin*(100*c)*weight]
    ##### Sensor stimulation parameters. (Go to data/sensoryNeuronTable1.jpg to choose rational combinations)
    area=[] ## Area: 'head', 'body', 'tail'. 
    LRb=[] ## LRb: 'L' (left), 'R' (right), 'b' (body).
    sensor=[] ## Sensor: 'oxygen', 'mechanosensor', 'propioSomatic', 'propioTail', 'propioPharynx',
             ## 'propioHead', 'chemosensor', 'osmoceptor', 'nociceptor', 'thermosensor', 'thermonociceptive'. 
    
    G, masterInfo, simInitActivity,  pathLength, hpTest, envActivation = simulation(timesteps, sim_no, ratioRandomInit, c, area, LRb, sensor, Psens, att)
    representation(G, masterInfo, sim_no, timesteps, simInitActivity)
    return masterInfo, envActivation


def paramTest():
    from _simulation_ import simulation
    import pandas
    
    ### Define simulation variables
    timesteps = 50
    sim_no = 10
    
    Psenss=[0.5, 0.75]   # Probability of sensory neurons being excited by environment
    
    
    ##### Sensor stimulation parameters. (Go to data/sensoryNeuronTable1.jpg to choose rational combinations)
    area=[] ## Area: 'head', 'body', 'tail'. 
    LRb=[] ## LRb: 'L' (left), 'R' (right), 'b' (body).
    sensor=[] ## Sensor: 'oxygen', 'mechanosensor', 'propioSomatic', 'propioTail', 'propioPharynx', 'odorsensor',
             ## 'propioHead', 'chemosensor', 'osmoceptor', 'nociceptor', 'thermosensor', 'thermonociceptive'. 
             
    ##Independent Variable 1 (RI)
    ratioRandomInit=[0.1,0.15,0.2] 
    
    
    ## Independent Variable 2 (c): free parameter influence of weights [exin*(100*c)*weight]
    clist=[0.07,0.08,0.09,0.1,0.11,0.12,0.13,0.14,0.15,
           0.16,0.17,0.18,0.19,0.20,0.21,0.25]

    ## Independent variable 3(att)
#    lis=list(range(-71,-80,-0.5))
    atts=[0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95]

    surviveTime={}  
    inATT={}
    rrp2rest={}
    envActiv={}
    
    for Psens in Psenss:
        surviveTime[Psens]={}
        inATT[Psens]={}
        rrp2rest[Psens]={} 
        envActiv[Psens]={}
        for ri in ratioRandomInit:
            surviveTime[Psens][ri]={}
            inATT[Psens][ri]={}
            rrp2rest[Psens][ri]={}
            envActiv[Psens][ri]={}
            for c in clist:
                surviveTime[Psens][ri][c]=pandas.DataFrame()
                inATT[Psens][ri][c]=pandas.DataFrame()
                rrp2rest[Psens][ri][c]=pandas.DataFrame()
                envActiv[Psens][ri][c]={}
    
                
                for att in atts:
                    G, masterInfo, simInitActivity, pathLength, hpTest, envActivation = simulation (timesteps, sim_no, ri, c, area, LRb, sensor, Psens, att)
                    
                    surviveTime[Psens][ri][c][att]=masterInfo['mainInfoGraded']['deactivated'].values()
                    surviveTime[Psens][ri][c][att]=surviveTime[Psens][ri][c][att].replace('None', timesteps)
                    
                    envActiv[Psens][ri][c][att]=envActivation
                    
                ### manipulate data to obtain probability of rrp to spike
                    inATTlist=[]
                    rrp2restList=[]
                    for sim in range(sim_no):
                        inATTcount=0
                        rrp2restCount=0
                        if masterInfo['mainInfoGraded']['deactivated'][sim]=='None':
                            for timestep in range(timesteps):
                                inATTcount+=hpTest[sim][timestep].count('inATT')
                                rrp2restCount+=hpTest[sim][timestep].count('rrp2rest')
                            ## compute probability of using the refractory period and add it to a list. 
                            inATTlist.append(inATTcount)
                            rrp2restList.append(rrp2restCount)
                        
                        else:
                            for timestep in range(masterInfo['mainInfoGraded']['deactivated'][sim]):
                                inATTcount+=hpTest[sim][timestep].count('inATT')
                                rrp2restCount+=hpTest[sim][timestep].count('rrp2rest')
                            ## compute probability of using the refractory period and add it to a list. 
                            inATTlist.append(inATTcount)
                            rrp2restList.append(rrp2restCount)
                    
                    inATT[Psens][ri][c][att]=inATTlist
                    rrp2rest[Psens][ri][c][att]=rrp2restList


    return masterInfo, surviveTime, inATT, rrp2rest, envActiv



'''

Launcher

'''

'''## standard simulation Launcher'''

#masterInfo, simInitActivity, pathLength, envActivation = standardInit()




'''## Activity simulation Launcher'''

import pandas
import time
from rasterPlot import rasterPlot
   
masterInfo, envActivation = activityInit()

## Export activity to a binary dataframe
actdf=pandas.DataFrame(masterInfo['mainInfoGraded']['activitydata'][0])
actdf=actdf.replace([-70,-69,-69.5,-65], 0)
actdf=actdf.replace(-30, 1)   
Activity=actdf.transpose()

## from Activity dataframe generate Raster plot
rasterPlot(Activity, envActivation)

#localtime = time.asctime(time.localtime(time.time()))
#Activity.to_csv('data/parameterTesting/Activity_'+localtime+'.csv', index=False)

del actdf



'''## Activity compose Launcher'''

#import pandas
#import time
#import networkx as nx
#
#Activity=pandas.DataFrame()
#T=0
#
#while T<100000:
#    
#    T,N=Activity.shape
#    
#    masterInfo, envActivation = activityInit()
#    
#    ## Export activity to a binary dataframe
#    actdf=pandas.DataFrame(masterInfo['mainInfoGraded']['activitydata'][0])
#    actdf=actdf.replace([-70,-69,-65], 0)
#    actdf=actdf.replace(-30, 1)   
#    actdf=actdf.transpose()
#    Activity=Activity.append(actdf)
#    
#Activity.index=range(len(Activity))     # reset indexes 
#
### Append cell names for analysis
#G = nx.read_graphml("data/elegans.herm_connectome.graphml")
#names=[]
#for n in list(Activity):
#    names.append(G.node[n]['cell_name'])
#
#Activity.loc[-1]=names
#Activity.index = Activity.index + 1     # shifting the index
#Activity=Activity.sort_index()
#
#localtime = time.asctime(time.localtime(time.time()))
#Activity.to_csv('data/parameterTesting/Activity_'+localtime+'.csv', index=False)
#
#del actdf, n, localtime, N, T




''' ## parameter Testing Launcher'''
#import pandas
#import time
#
#paramTestData=pandas.DataFrame()
#
### Run simulations
#masterInfo, surviveTime, inATT, rrp2rest, envActiv= paramTest()
#
### Gather data from simulations
#for Psens, ris in surviveTime.items():
#    for ri, cs in ris.items():
#        for c, atts in cs.items():
#            for att in list(surviveTime[Psens][ri][c]):
#                for i in list(surviveTime[Psens][ri][c].index):
#                    dic={'Psens':Psens,'RI':ri,'c':c,'att':att,'surviveTime':surviveTime[Psens][ri][c][att][i],
#                         'inATT':inATT[Psens][ri][c][att][i], 'rrp2rest':rrp2rest[Psens][ri][c][att][i],
#                         'active':len(envActiv[Psens][ri][c][att][i]['active']),'activeG':len(envActiv[Psens][ri][c][att][i]['activeG']),
#                         'activeSG':len(envActiv[Psens][ri][c][att][i]['activeSG']),'activeNode':len(envActiv[Psens][ri][c][att][i]['activeNode'])}
#                    
#                    paramTestData=paramTestData.append(dic, ignore_index=True)
#
### Export data to .csv
#localtime = time.asctime(time.localtime(time.time()))
#paramTestData.to_csv('data/parameterTesting/dataG_'+localtime+'.csv', index=False)
#
### Clear variables
#del c, cs, att, atts, ri, dic, i, localtime, surviveTime, Psens
#del envActiv, inATT, rrp2rest, ris


            