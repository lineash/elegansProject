#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 14:12:18 2019

@author: jescab01
"""

#export strange cases
def exportAnomalies(mainInfo, simInitActivity, c):
    
    import pandas
    import time
    
    
    localtime = time.asctime( time.localtime(time.time()) )
    
    weirdActivity=pandas.DataFrame(mainInfo['activitydata'][0])
    
    weirdActivity.to_csv('output/weirdActivities/weirdActivity['+str(simInitActivity[0])+']['+str(c)+']'+localtime+'.csv')
    

def exportParamTest(paramTestDic):
    
    import pandas
    
    dfDic={}
    
    for testDic, data in paramTestDic.items():
        dfDic[testDic]={}
        for RI, RIdata in data.items():
            df=pandas.DataFrame()
            for c, cdata in RIdata.items():
                cdatalist=list(cdata.values())
                df[c]=cdatalist
            dfDic[testDic]['RI'+str(RI)]=df
            
        for tests, RIs in dfDic.items():    
            for RI, data in RIs.items():
                data.to_csv('data/parameterTesting/experimentalData/'+tests+'/'+RI+'.csv', index=False)
                    
                    
 ### clear folders
def clearParamTestfolders():
     
    import os
    
    dirList = os.listdir('data/parameterTesting/experimentalData')
    
    for fold in dirList:
        fileList=os.listdir('data/parameterTesting/experimentalData/'+fold)
        
        for file in fileList:
            os.remove('data/parameterTesting/experimentalData/'+fold+'/'+file)

    
    
    
                    