#!/usr/bin/env python3
import json
from zipfile import ZipFile
import io
import pandas as pd
import os
import numpy as np
from Bio.Seq import Seq
import rich


def grabZipCount(inputzip):
    dataStr = inputzip.split('/')[-1].split('.')[0] + "/fastqc_data.txt"
    with ZipFile(inputzip) as z:
        with z.open(dataStr) as f:
            qcData = io.TextIOWrapper(f, newline='\n')
            for line in qcData:
                if line.startswith('Total'):
                    return int(line.strip().split()[2])


def revC(string):
    return str(Seq(string).reverse_complement())


def parseSS(ss):
    ssdf = pd.read_csv(ss, comment='[')
    ssdf = ssdf.dropna()
    ssdf = ssdf.replace(' ', '_', regex=True)
    # Fetch the total number of reads per sample
    readCount = []
    for index, row in ssdf.iterrows():
        projID = "Project_" + row['Sample_Project']
        sampleID = "Sample_" + row['Sample_ID']
        sampleName = row['Sample_Name']
        zipStr = os.path.join("FASTQC_" + projID,
                              sampleID,
                              sampleName + "_R1_fastqc.zip")
        if os.path.exists(zipStr):
            readCount.append(grabZipCount(zipStr))
        else:
            rich.print("Warning, {} not found.".format(zipStr))
            readCount.append(0)
    ssdf['readCount'] = readCount
    if 'index2' in ssdf.columns:
        pairedStatus = True
    else:
        pairedStatus = False
    return ssdf, pairedStatus


def parseUnd(statFile, depth):
    with open(statFile) as f:
        stats = json.load(f)
        candidates = {}
        for lane in stats['UnknownBarcodes']:
            for comb in lane['Barcodes']:
                if np.round(
                    depth/lane['Barcodes'][comb]) == 1 or \
                   depth < lane['Barcodes'][comb]:
                    if comb not in candidates:
                        candidates[comb] = lane['Barcodes'][comb]
        return candidates

def crapMatcher(ssdf, pairedStatus, candidates, depth):
    # Fetch the combinations in candidates.
    # if pairedStatus == True:
    candNes = []
    for indexPair in candidates:
        candNes.append([
            indexPair.split('+')[0],
            indexPair.split('+')[1]
        ])
    samplesDic = {}
    for index, row in ssdf[ssdf['readCount'] < depth].iterrows():
        samplesDic[row['Sample_Name']] = [
            row['index'],
            row['index2']
        ]
    updateDic = {}
    for failure in samplesDic:
        for candidate in candNes:
            if samplesDic[failure][0] in candidate and revC(samplesDic[failure][1]) in candidate:
                updateDic[failure] = candidate
    updateDF = ssdf
    for update in updateDic:
        updateDF.loc[updateDF['Sample_Name'] == update, 'index'] = updateDic[update][0]
        updateDF.loc[updateDF['Sample_Name'] == update, 'index2'] = updateDic[update][1]
    del updateDF['readCount']
    return updateDF, len(updateDic)
