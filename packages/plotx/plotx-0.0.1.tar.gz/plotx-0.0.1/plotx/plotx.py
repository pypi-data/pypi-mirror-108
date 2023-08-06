# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 13:01:39 2021

@author: DaveAstator
"""

import matplotlib.pyplot as plt;
import numpy as np;
            
def UniformDots2D(x,y):
    low = np.min(np.concatenate((x,y)))
    high = np.max(np.concatenate((x,y)))
    plt.xlim(low, high)
    plt.ylim(low, high)
    plt.scatter(x,y)
    
def ValOrNone(key,dic):
    if key in dic:
        return dic[key]
    else:
        return None
    
def UniformDots3D_p(plotData):
    c = ValOrNone('c' , plotData);
    s = ValOrNone('s' , plotData);
    x = ValOrNone('x' , plotData);
    y = ValOrNone('y' , plotData);
    z = ValOrNone('z' , plotData);
    a = ValOrNone('a' , plotData);
    UniformDots3D(x,y,z,c,s,a)
    
def UniformDots3D(x,y,z,c = None, s = None, a = 1):
    print('3d point plot',s)
    
    if s == None:
        s = plt.rcParams['lines.markersize'] ** 2
        
    if a == None:
        a = 1

        
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    low = np.min(np.concatenate((x,y,z)))
    high = np.max(np.concatenate((x,y,z)))
    
    ax.set_xlim(low, high)
    ax.set_ylim(low, high)
    ax.set_zlim(low, high)
    ax.set_box_aspect((1, 1, 1)) 
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    ax.scatter(x,y,z, c=c, s=s, alpha = a)
    plt.show()  

def dots(data, cypher):
    valDict = toPlotData(data,cypher)
    
    ndim = int('x' in cypher) + int('y' in cypher) + int('z' in cypher)

    if ndim <= 1:
        plt.plot(valDict['x'])
    if ndim == 2:
        UniformDots2D(valDict['x'],valDict['y'])
    if ndim == 3:
        UniformDots3D_p(valDict)

def toPlotData(data, cypher):
    valDict = {}
    bins = cypher.split(',')
    row = 0

    subDimId = 0
    for b in bins:
        if len(bins) ==1:
            bvals = data
        else:
            bvals = data[row]
        row = row + 1
    
        for dim in b:
            if type(bvals) is list:
                if type(bvals[0]) is list:
                    valDict[dim] = [p[subDimId] for p in bvals]
                else:
                    #valDict[dim] = [p for p in bvals]
                    valDict[dim] = bvals[subDimId]
            else:
                valDict[dim] = bvals
                
            subDimId = subDimId + 1
        subDimId = 0
    return valDict


data = [[[1,2,3],[2,3,20],[5,5,11]],[1,2,3],[403,8]]
dots(data,'zxy,c,s')


cypher = 'zxy,c,s'
valDict = {}
bins = cypher.split(',')

row = 0
subDimId = 0
for b in bins:
    if len(bins) ==1:
        bvals = data
    else:
        bvals = data[row]
    row = row + 1

    for dim in b:
        if type(bvals) is list:
            if type(bvals[0]) is list:
                valDict[dim] = [p[subDimId] for p in bvals]
            else:
                valDict[dim] = [p for p in bvals]
                #valDict[dim] = bvals[subDimId]
        else:
            valDict[dim] = bvals
            
        subDimId = subDimId + 1
    subDimId = 0





            
    