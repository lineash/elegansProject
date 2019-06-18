'''

Specifying functions for whole connectome

'''

def infoM(G, sim_no):
    mainInfo={'activitydata':{}, 'fireCount': {}, 'deactivated': {}}
    for sim in range(sim_no):
        mainInfo['activitydata'][sim]={}
        mainInfo['fireCount'][sim]={}
        mainInfo['deactivated'][sim]='None'
        for n,nbrs in G.adj.items():
            mainInfo['fireCount'][sim][n] = 0            
    return mainInfo
        


def mainWorm(G, sim, timesteps, initActivity, activityDic, activity, mainInfo, c, hpV, hpTest, Psens, envActivation):
    
    from envInput import randomSensInput
    
         ### assign initial activity to nodes as attribute   
    for i in range(302):
        G.node['n'+str(i)]['mV']=initActivity[sim]['n'+str(i)]
        
        ### run specific simulation for timesteps
    for i in range(timesteps):
        chemtime = i-3          ## Define temporal difference between electrical and chemical synapses
        if chemtime>=0:    
            chemdata = []
            for a in range(302):
                chemdata.append(mainInfo['activitydata'][sim][chemtime]['n'+str(a)])
            if sum(activity)/302 == -70:
                if sum(chemdata)/302 == -70:
                    mainInfo['deactivated'][sim]= i
                    print('Main network deactivation at: simulation ' + str(sim) + ', time ' + str(i) +'.')
                    break
        mainInfo['activitydata'][sim][i] = activityDic
        hpTest[sim][i]=[]
        hpTest[sim][i]=single_time_step(G, sim, i, mainInfo, chemtime, c, hpV, hpTest[sim][i])
        envActivation=randomSensInput(G, Psens, sim, envActivation, i)
        activity, activityDic = getActivity(G)
    
    ##removing last row of hpTest=='inRRP' 
    for a in range(302):
        if mainInfo['deactivated'][sim]=='None':
            for i in range(len(hpTest[sim][timesteps-1])):
                if hpTest[sim][timesteps-1][i]=='inRRP':
                    hpTest[sim][timesteps-1].remove('inRRP')
                    break
    
        else: 
            timeplt=mainInfo['deactivated'][sim]-1
            for i in range(len(hpTest[sim][timeplt])):
                if hpTest[sim][timeplt][i]=='inRRP':
                    hpTest[sim][timeplt].remove('inRRP')
                    break

    return mainInfo, hpTest, envActivation



def getActivity(G):
    activity = []
    activityDic={}
    for n,nbrs in G.adj.items():
        activity.append(G.node[n]['mV'])
    for i in range(302):
        activityDic['n'+str(i)]=G.node['n'+str(i)]['mV']
    return activity, activityDic



def single_time_step(G, sim, timestep, mainInfo, chemtime, c, hpV, hpTest):  
    
    integral= [0] * G.number_of_nodes()
    m = 0
    
    for n,nbrs in G.adj.items():
        if G.node[n]['mV'] == 40: 		
            G.node[n]['mV'] = -60
            
        elif G.node[n]['mV'] == -60: 		
            G.node[n]['mV'] = hpV
            hpTest.append('inRRP')        
		
		#determine input from neighbours and decide if the integral is sufficient for firing	
        elif G.node[n]['mV']!=40 and G.node[n]['mV'] != -60:
            for nbr,eattr in nbrs.items():
                if chemtime >= 0: 
                    if eattr['Esyn']=='True' and eattr['Csyn']=='True':
                        if mainInfo['activitydata'][sim][timestep][nbr]==40 and mainInfo['activitydata'][sim][chemtime][nbr] == 40:
                            integral[m] +=  G.node[nbr]['exin'] * mainInfo['activitydata'][sim][timestep][nbr]*c * eattr['EnormWeight']
                            integral[m] +=  G.node[nbr]['exin'] * mainInfo['activitydata'][sim][chemtime][nbr]*c * eattr['CnormWeight']
                            
                        if mainInfo['activitydata'][sim][timestep][nbr]==40:
                            integral[m] +=  G.node[nbr]['exin'] * mainInfo['activitydata'][sim][timestep][nbr]*c * eattr['EnormWeight']
                            
                        if mainInfo['activitydata'][sim][chemtime][nbr] == 40:
                            integral[m] +=  G.node[nbr]['exin'] * mainInfo['activitydata'][sim][chemtime][nbr]*c * eattr['CnormWeight']
                            
    
                    elif eattr['Esyn'] == 'True' and mainInfo['activitydata'][sim][timestep][nbr]==40:
                        integral[m] +=  G.node[nbr]['exin'] * mainInfo['activitydata'][sim][timestep][nbr]*c * eattr['EnormWeight']
                    
                    elif eattr['Csyn'] == 'True' and mainInfo['activitydata'][sim][chemtime][nbr] == 40:
                        integral[m] +=  G.node[nbr]['exin'] * mainInfo['activitydata'][sim][chemtime][nbr]*c * eattr['CnormWeight']
                        
                        
                else: 
                    if eattr['Esyn'] == 'True' and mainInfo['activitydata'][sim][timestep][nbr]==40:
                        integral[m] +=  G.node[nbr]['exin'] * mainInfo['activitydata'][sim][timestep][nbr]*c * eattr['EnormWeight']
              
                    
            if integral[m]+G.node[n]['mV'] > -55:
                G.node[n]['mV'] = 40
                mainInfo['fireCount'][sim][n] += 1 
                
                
            elif G.node[n]['mV'] == hpV: 		#relative refractory period in one timestep
                G.node[n]['mV'] = -70
                hpTest.append('rrp2rest')
                
		#for tracking the integral list		
        m += 1
       
    return hpTest

