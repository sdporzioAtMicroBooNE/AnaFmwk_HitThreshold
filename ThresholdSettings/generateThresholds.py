import numpy as np
import pandas as pd

def makeThresholds(thres):
    fThres = []
    sThres = []
    for i in range(len(thres)):
        fThres.append([float('%.4s' %val) for val in thres[i]])
        sThres.append('%.4s_%.4s_%.4s' %tuple(thres[i]))

    fThres = pd.DataFrame(fThres,columns=['u','v','y'])
    fThres.to_csv('fThres.csv',index=False)
    sThres = pd.DataFrame(sThres,columns=['String'])
    sThres.to_csv('sThres.csv',index=False)

# Original Thresholds
origThres = np.array([2.6,2.6,3.25])

# Default Thresholds
defThresholds = [
    [1.0, 1.0, 1.0],
    [1.82, 1.82, 2.275],
    [2.08, 2.08, 2.6],
    [2.34, 2.34, 2.925],
    [2.6, 2.6, 3.25],
    [2.86, 2.86, 3.575],
    [3.12, 3.12, 3.9],
    [3.38, 3.38, 4.225],
    [5.0, 5.0, 5.0]
]

# Multiplication Thresholds
multThresholds = [[1.0,1.0,1.0]]
mult = np.concatenate((np.linspace(0.5,1,4,endpoint=False),np.linspace(1,2,4)))
for i in range(len(mult)):
    multThresholds.append(origThres*mult[i])

# Low Thresholds
lowThresholds = [
    [0.5, 0.5, 0.5],
    [0.6, 0.6, 0.6],
    [0.7, 0.7, 0.7],
    [0.8, 0.8, 0.8],
    [0.9, 0.9, 0.9],
    [1.0, 1.0, 1.0],
    [1.2, 1.2, 1.2],
    [1.5, 1.5, 1.5]
]

makeThresholds(lowThresholds)
