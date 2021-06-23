import glob
import numpy as np
import argparse
import sys
import pandas as pd




resDic = {}
resDic['human'] = {}
resDic['fly'] = {}
resDic['mouse'] = {}

for i in glob.glob('*/*/*.markdup.txt'):
    org = str(i).split('/')[0].replace('OUT','')
    name = str(i).split('/')[-1].replace('.markdup.txt','')
    if name not in resDic[org]:
        resDic[org][name] = {}
    with open(i) as f:
        for line in f:
            if 'in total' in line:
                resDic[org][name]['totalReads'] = int(line.split(' ')[0]) 
            if 'mapped (' in line:
                resDic[org][name]['mapFrac'] = int(line.split(' ')[0])/resDic[org][name]['totalReads']
            if 'duplicates' in line:
                resDic[org][name]['dupFrac'] = int(line.split(' ')[0])/resDic[org][name]['totalReads']
tempDic = {}
for i in resDic:
    if i not in tempDic:
        tempDic[i] = {}
    for sample in resDic[i]:
        if '100ng' not in sample:
            if 'low' not in tempDic[i]:
                tempDic[i]['low'] = {}
                tempDic[i]['low']['mapFrac'] = [resDic[i][sample]['mapFrac']]
                tempDic[i]['low']['dupFrac'] = [resDic[i][sample]['dupFrac']]
            else:
                tempDic[i]['low']['mapFrac'].append(resDic[i][sample]['mapFrac'])
                tempDic[i]['low']['dupFrac'].append(resDic[i][sample]['dupFrac'])
        if '100ng' in sample:
            if 'high' not in tempDic[i]:
                tempDic[i]['high'] = {}
                tempDic[i]['high']['mapFrac'] = [resDic[i][sample]['mapFrac']]
                tempDic[i]['high']['dupFrac'] = [resDic[i][sample]['dupFrac']]
            else: 
                tempDic[i]['high']['mapFrac'].append(resDic[i][sample]['mapFrac'])
                tempDic[i]['high']['dupFrac'].append(resDic[i][sample]['dupFrac'])


qcScreenDic = {}
for i in glob.glob('*FQSCR/*R1_screen.txt'):
    org = i.split('/')[0].replace('FQSCR','')
    if org == 'fly':
        baitList = ['Drosophila', 'flyrRNA', 'flyMito']
    elif org == 'mouse':
        baitList = ['Mouse', 'mouserRNA', 'mouseMito']
    elif org == 'human':
        baitList = ['Human', 'humanrRNA', 'humanMito']
    else:
        print("No idea what organism this is lol")
        sys.exit()
    if org not in qcScreenDic:
        qcScreenDic[org] = {}
    if '100ng' in i:
        InputN = 'high'
    elif '10ng' in i:
        InputN = 'low'
    elif '25ng' in i:
        InputN = 'low'
    else:
        print("cant see input wtf: {}".format(i))
        sys.exit()
    if InputN not in qcScreenDic[org]:
        qcScreenDic[org][InputN] = {}
        qcScreenDic[org][InputN]['Mito'] = []
        qcScreenDic[org][InputN]['rRNA'] = []
        qcScreenDic[org][InputN]['Genome'] = []
    with open(i) as f:
        for line in f:
            if line.strip() != '':
                if line.strip().split()[0] in baitList:
                    if 'Mito' in line.strip().split()[0]:
                        qcScreenDic[org][InputN]['Mito'].append(float(line.strip().split()[5] ) + float( line.strip().split()[7] ) +  float( line.strip().split()[9] ) )
                    elif 'rRNA' in line.strip().split()[0]:
                        qcScreenDic[org][InputN]['rRNA'].append(float(line.strip().split()[5] ) + float( line.strip().split()[7] )  + float( line.strip().split()[9] ) )
                    else:
                        qcScreenDic[org][InputN]['Genome'].append(float(line.strip().split()[5] ) + float( line.strip().split()[7] ) + float(line.strip().split()[9] ) + float (line.strip().split()[11]) )

for i in glob.glob('*/deepTools_qc/plotEnrichment/plotEnrichment.tsv'):
    org = str(i).split('/')[0].replace('OUT','')
    tempDic[org]['low']['geneFrac'] = []
    tempDic[org]['high']['geneFrac'] = []
    with open(i) as f:
        for line in f:
            if line.strip().split()[1] == 'gene':
                name = line.strip().split()[0]
                print(name)
                if '100ng' not in name:
                    tempDic[org]['low']['geneFrac'].append(float(line.strip().split()[2]))
                if '100ng' in name:
                    tempDic[org]['high']['geneFrac'].append(float(line.strip().split()[2]))

for i in glob.glob("*/featureCounts/*.counts.txt"):
    org = str(i).split('/')[0].replace('OUT','')
    if '100ng' not in i:
        if 'geneCov' not in tempDic[org]['low']:
            tempDic[org]['low']['geneCov'] = []
        tempDF = pd.read_csv(i, sep='\t', comment='#', header=0)
        tempDF.columns = ['Geneid', 'Chr', 'Start', 'End', 'Strand', 'Length', 'Count']
        print(str(len(tempDF[tempDF['Count'] != 0])/len(tempDF)))



print("{}\t{}\t{}\t{}\t{}\t{}\t{}".format('organism','sampleType', 'genome%', 'duplication%','rRNA%', 'Mito%', 'Gene%'))
for org in tempDic:
    print("{}\t{}\t{}\t{}\t{}\t{}\t{}".format(org, 'low Input',
                              str(np.round(np.mean(qcScreenDic[org]['low']['Genome']), 2 )) + '±' + str(np.round(np.std(qcScreenDic[org]['low']['Genome']), 2)),
                              str(np.round(np.mean(tempDic[org]['low']['dupFrac']) * 100, 2)) + '±' + str(np.round(np.std(tempDic[org]['low']['dupFrac']) * 100,2)),
                              str(np.round(np.mean(qcScreenDic[org]['low']['rRNA']), 2 )) + '±' + str(np.round(np.std(qcScreenDic[org]['low']['rRNA']), 2)),
                              str(np.round(np.mean(qcScreenDic[org]['low']['Mito']), 2 )) + '±' + str(np.round(np.std(qcScreenDic[org]['low']['Mito']), 2)),
                              str(np.round(np.mean(tempDic[org]['low']['geneFrac']), 2 )) + '±' + str(np.round(np.std(tempDic[org]['low']['geneFrac']), 2)),
                             )
         )
    print("{}\t{}\t{}\t{}\t{}\t{}\t{}".format(org, 'high Input',
                              str(np.round(np.mean(qcScreenDic[org]['high']['Genome']), 2 )) + '±' + str(np.round(np.std(qcScreenDic[org]['high']['Genome']), 2)),
                              str(np.round(np.mean(tempDic[org]['high']['dupFrac']) * 100, 2)) + '±' + str(np.round(np.std(tempDic[org]['high']['dupFrac']) * 100,2)),
                              str(np.round(np.mean(qcScreenDic[org]['high']['rRNA']), 2 )) + '±' + str(np.round(np.std(qcScreenDic[org]['high']['rRNA']), 2)),
                              str(np.round(np.mean(qcScreenDic[org]['high']['Mito']), 2 )) + '±' + str(np.round(np.std(qcScreenDic[org]['high']['Mito']), 2)),
                              str(np.round(np.mean(tempDic[org]['high']['geneFrac']), 2 )) + '±' + str(np.round(np.std(tempDic[org]['high']['geneFrac']), 2)),
                             )
         )

