import os, sys, argparse, ROOT
import numpy as np
import pandas as pd
from collections import OrderedDict as OD

def Warning(string):
    START_W = '\033[1;33m'
    END_W = '\033[0m'
    print START_W + string + END_W

def ExtractThresholdsFromName(path,extension):
    # Path sample: HitThreshold/Analysis/TrackLengthAnalysis/Data/MCC7/MC/histoFile_Tracy_AnaReco_1.62_1.62_2.03.root
    dataVersion = path.split('/')[-3]
    dataType = path.split('/')[-2]
    fileName = path.split('/')[-1]
    fileName = fileName.replace(extension,'') # Remove extension
    dataInd = [-3,-2,-1]
    thres = tuple([fileName.split('_')[i] for i in dataInd]) # Get 3 final substrings
    return thres,dataType,dataVersion

def Hist2Array(histo):
    array = [[],[]]
    n = histo.GetNbinsX()
    for i in range(n):
        array[0].append(histo.GetBinLowEdge(i+1))
        array[1].append(histo.GetBinContent(i+1))
    npArr = np.array(array)
    return npArr

def ExtractTrackLength(inDir,outDir,extension):
    fileNames = [inDir+fileName for fileName in os.listdir(inDir) if extension in fileName[-1*len(extension):]]

    for fileName in fileNames:
        Warning('Analyzing %s' %fileName)
        thres,dataType,dataVersion = ExtractThresholdsFromName(fileName,extension)
        tFile = ROOT.TFile(fileName,"READ")
        tDir = tFile.Get('TrackHitAna').Get('FitTrackHits')
        tHist = tDir.Get('TrackLength')
        arr = Hist2Array(tHist)
        data = OD([
                ('TrackLength',arr[0]),
                ('Count',arr[1])
            ])
        outData = pd.DataFrame(data)
        outData.to_csv(outDir+'%s_%s_trackLength_%s_%s_%s.csv' %(dataVersion,dataType,thres[0],thres[1],thres[2]),index=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input',required=True,help='Input directory',type=str)
    parser.add_argument('-o','--output',required=False,default='Output',help='Output directory',type=str)
    parser.add_argument('-e','--extension',required=False,default='.root',help='File extension',type=str)
    args = parser.parse_args()
    if args.input[-1]!='/':
        args.input += '/'
    if args.output[-1]!='/':
        args.output += '/'
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    ExtractTrackLength(args.input,args.output,args.extension)

if __name__ == '__main__':
    main()
