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

def Hist1d2Array(histo):
    array = [[],[],[]]
    n = histo.GetNbinsX()
    for i in range(n):
        array[0].append(histo.GetBinLowEdge(i+1))
        array[1].append(histo.GetBinContent(i+1))
    return array

def Hist2d2Array(histo):
    nx = histo.GetNbinsX()
    ny = histo.GetNbinsY()
    array = [np.empty([nx]),np.empty([ny]),np.empty([nx,ny])]
    for i in range(nx):
        array[0][i] = histo.GetXaxis().GetBinLowEdge(i+1)
    for j in range(ny):
        array[1][j] = histo.GetYaxis().GetBinLowEdge(j+1)
    for i in range(nx):
        for j in range(ny):
            array[2][i][j] = histo.GetBinContent(i+1,j+1)
    return array

def Plot2dHitsHisto(inDir,jobType,histoName='PHVsWidth'):
    # Settings
    col = ['r','g','b']
    titles = ['U plane','V plane','Y plane']
    subs = ['FitTrackHits','PFPartHits','AllHits']
    subNames = ['Track Hits','PFPart Hits','All (other) Hits']
    xlab = 'PH [ADC]'
    ylab = 'Width [TDC]'

    if not inDir[-1]=='/': inDir+='/'
    fileNames = [inDir+fileName for fileName in os.listdir(inDir) if '.root' in fileName[-5:]]

    rootFile = ROOT.TFile(fileNames[0],'READ')
    rootDir = rootFile.Get('TrackHitAna')
    rootSub = rootDir.Get(subs[0])
    rootHisto = rootSub.Get(histoName+'0')
    refMap2D = Hist2d2Array(rootHisto)
    nx = len(refMap2D[0])
    ny = len(refMap2D[1])

    for k,sub in enumerate(subs):
        fig = [[],[],[]]
        canv = plt.figure(figsize=(15,5))
        for plane in range(3):
            mapSum = [np.zeros([nx]),np.zeros([ny]),np.zeros([nx,ny])]
            for i in range(nx):
                mapSum[0][i] = refMap2D[0][i]
            for j in range(ny):
                mapSum[1][j] = refMap2D[1][j]
            for fileName in fileNames:
                rootFile = ROOT.TFile(fileName,'READ')
                rootDir = rootFile.Get('TrackHitAna')
                rootSub = rootDir.Get(sub)
                rootHisto = rootSub.Get(histoName+'%i' %plane)
                map2D = Hist2d2Array(rootHisto)
                for i in range(nx):
                    for j in range(ny):
                        mapSum[2][i][j] += map2D[2][i][j]
            fig[plane] = canv.add_subplot(131+plane)
            plt.pcolormesh(mapSum[0],mapSum[1],mapSum[2].T,cmap='RdYlBu_r')
            plt.title(jobType+' | '+subNames[k]+'\n'+titles[plane]+'\n')
            if plane==2:
                plt.axvline(3.25,color='black',lw=3,ls='--')
            else:
                plt.axvline(2.6,color='black',lw=3,ls='--')
            plt.xlabel(xlab)
            plt.xlim(1,20.)
            plt.colorbar()
        fig[0].set_ylabel(ylab)
        plt.show()
    af.End()

def Plot1dHitsHisto(inDir,jobType,histoName='PulseHeightS',xlab='PH [ADC]',xlim=100.):
    # Settings
    col = ['r','g','b']
    titles = ['U plane','V plane','Y plane']
    subs = ['FitTrackHits','PFPartHits','AllHits']
    subNames = ['Track Hits','PFPart Hits','All (other) Hits']

    if not inDir[-1]=='/': inDir+='/'
    fileNames = [inDir+fileName for fileName in os.listdir(inDir) if '.root' in fileName[-5:]]

    rootFile = ROOT.TFile(fileNames[0],'READ')
    rootDir = rootFile.Get('TrackHitAna')
    rootSub = rootDir.Get(subs[0])
    rootHisto = rootSub.Get(histoName+'0')
    refMap2D = Hist1d2Array(rootHisto)
    nx = len(refMap2D[0])

    for k,sub in enumerate(subs):
        fig = [[],[],[]]
        canv = plt.figure(figsize=(15,5))
        for plane in range(3):
            mapSum = [np.zeros([nx]),np.zeros([nx])]
            for i in range(nx):
                mapSum[0][i] = refMap2D[0][i]
            for fileName in fileNames:
                rootFile = ROOT.TFile(fileName,'READ')
                rootDir = rootFile.Get('TrackHitAna')
                rootSub = rootDir.Get(sub)
                rootHisto = rootSub.Get(histoName+'%i' %plane)
                map2D = Hist1d2Array(rootHisto)
                for i in range(nx):
                    mapSum[1][i] += map2D[1][i]
            dof = len(mapSum[0])-4
            fig[plane] = canv.add_subplot(131+plane)
            plt.plot(mapSum[0],mapSum[1],color=col[plane],lw=1,drawstyle='steps')
            plt.title(jobType+' | '+subNames[k]+'\n'+titles[plane]+'\n')
            plt.xlabel(xlab)
            plt.xlim(0,xlim)
            plt.grid(True)
            if 'PulseHeight' in histoName:
                if plane==2:
                    plt.axvline(3.25,color='black',lw=3,ls='--')
                else:
                    plt.axvline(2.6,color='black',lw=3,ls='--')
        plt.show()
    af.End()
