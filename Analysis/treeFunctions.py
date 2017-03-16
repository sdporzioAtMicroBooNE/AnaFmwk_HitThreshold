import os, sys, json, ROOT
import numpy as np
import pandas as pd
import root_numpy as rnp
import matplotlib.pyplot as plt
import auxFunctions as af
from collections import OrderedDict as OD
from ipywidgets import interact, interactive, fixed, widgets
from NotebookUtils.ProgressBar import LogProgress as LP
plt.rcParams['font.family']='serif'
plt.rcParams['font.weight']='light'
plt.rcParams['font.size']=10
figsize = (16,8)

# Settings
planes = ['U','V','Y','Total']
colors = ['red','blue','green','orange','purple']
lengths = [150,200,250]
endT = 20.
thresholds = np.linspace(1.0,endT,50)

def Pandafy(fileName, tree):
    df = pd.DataFrame(rnp.root2array(fileName,tree))
    return df

def ConcatenateRoot(inDir,tree,nFiles=-1):
    if not inDir[-1]=='/': inDir+='/'
    fileNames = []
    if nFiles==-1:
        fileNames = [inDir+fileName for fileName in os.listdir(inDir) if '.root' in fileName[-5:]]
    else:
        fileNames = [inDir+fileName for fileName in os.listdir(inDir)[:nFiles] if '.root' in fileName[-5:]]
    df_v = [Pandafy(fileName,tree) for fileName in fileNames]
    df = pd.concat(df_v,ignore_index=True)
    af.End()
    return df

def GetCompletenessDf(rootDf,tLength,thres):
    dataHits = [[],[],[],[]]
    dictHits = [0,0,0,0]
    dictPlanes = [0,0,0,0]
    if tLength!=0: longTracks = rootDf[rootDf['TrackLength']>tLength]
    else: longTracks = rootDf
    for i,longTrack in longTracks.iterrows():
        nHitsU = len(longTrack['Hit_PulseHeight_U'])
        nHitsV = len(longTrack['Hit_PulseHeight_V'])
        nHitsY = len(longTrack['Hit_PulseHeight_Y'])
        nHitsU_cut = len(longTrack['Hit_PulseHeight_U'][longTrack['Hit_PulseHeight_U']>thres])
        nHitsV_cut = len(longTrack['Hit_PulseHeight_V'][longTrack['Hit_PulseHeight_V']>thres])
        nHitsY_cut = len(longTrack['Hit_PulseHeight_Y'][longTrack['Hit_PulseHeight_Y']>thres])
        if nHitsU==0: compU = float('nan')
        else: compU = nHitsU_cut/float(nHitsU)
        if nHitsV==0:compV = float('nan')
        else: compV = nHitsV_cut/float(nHitsV)
        if nHitsY==0: compY = float('nan')
        else: compY = nHitsY_cut/float(nHitsY)
        if (nHitsU+nHitsV+nHitsY)==0: compTot = float('nan')
        else: compTot = (nHitsU_cut+nHitsV_cut+nHitsY_cut)/float(nHitsU+nHitsV+nHitsY)
        dataHits[0].append([compU,nHitsU,nHitsU_cut,longTrack['TrackID'],longTrack['Event']])
        dataHits[1].append([compV,nHitsV,nHitsV_cut,longTrack['TrackID'],longTrack['Event']])
        dataHits[2].append([compY,nHitsY,nHitsY_cut,longTrack['TrackID'],longTrack['Event']])
        dataHits[3].append([
                compTot,
                nHitsU+nHitsV+nHitsY,
                nHitsU_cut+nHitsV_cut+nHitsY_cut,
                longTrack['TrackID'],
                longTrack['Event']
            ])

    for i in range(4):
        dictHits[i] = OD([
                ('Event',np.array(dataHits)[i,:,4]),
                ('TrackID',np.array(dataHits)[i,:,3]),
                ('Completeness',np.array(dataHits)[i,:,0]),
                ('NumHits',np.array(dataHits)[i,:,1]),
                ('NumHits_Cut',np.array(dataHits)[i,:,2])
            ])
    dictPlanes =  OD([
            ('U',dictHits[0]),
            ('V',dictHits[1]),
            ('Y',dictHits[2]),
            ('Total',dictHits[3])
        ])
    hitDf = pd.DataFrame(dictPlanes)
    return hitDf

def CompletenessMean(rootDf,plane,tLength,thres):
    hitDf = GetCompletenessDf(rootDf,tLength,thres)
    return np.nanmean(hitDf[plane]['Completeness'])

def PlotAll(rootDf_track,rootDf_others,jobType):
    plt.rcParams['font.size']=10
    canv = plt.figure(figsize=figsize)
    ax = [0,0,0,0]
    for i,plane in enumerate(planes[:-1]):
        ax[i] = canv.add_subplot(131+i)
        ax[i].set_title(jobType+' | %s plane' %plane)
        ax[i].set_xlabel('Threshold')
        if i==2:
            plt.axvline(3.25,color='black',lw=3,ls='--')
        else:
            plt.axvline(2.6,color='black',lw=3,ls='--')
        completeness_others = [CompletenessMean(rootDf_others,plane,0,t) for t in thresholds]
        plt.plot(thresholds,completeness_others,color='black',lw=3,label='Other hits')
        for j,length in enumerate(LP(lengths)):
            completeness_track = [CompletenessMean(rootDf_track,plane,length,t) for t in thresholds]
            plt.plot(thresholds,completeness_track,color=colors[j],lw=2,label='>%i cm' %length)
            plt.ylim(0.,1.)
            plt.xlim(1.,endT)
            plt.grid()
    ax[0].set_ylabel('Completeness')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, ncol=5)
    af.End()

def PlotEach(rootDf_track,rootDf_others,jobType):
    plt.rcParams['font.size']=15
    for i,plane in enumerate(planes[:-1]):
        canv = plt.figure(figsize=figsize)
        plt.title(jobType+' | %s plane' %plane)
        plt.xlabel('Threshold')
        plt.ylabel('Completeness')
        plt.xlim(1.,endT)
        if i==2:
            plt.axvline(3.25,color='black',lw=3,ls='--')
        else:
            plt.axvline(2.6,color='black',lw=3,ls='--')
        completeness_others = [CompletenessMean(rootDf_others,plane,0,t) for t in thresholds]
        plt.plot(thresholds,completeness_others,color='black',lw=3,marker='o',label='Other hits')
        for j,length in enumerate(LP(lengths)):
            completeness_track = [CompletenessMean(rootDf_track,plane,length,t) for t in thresholds]
            plt.plot(thresholds,completeness_track,color=colors[j],marker='o',lw=2,label='>%i cm' %length)
            plt.grid()
            plt.legend(loc='best')
    af.End()
