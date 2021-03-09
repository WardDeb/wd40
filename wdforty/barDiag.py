#!/usr/bin/env python3
import json
from zipfile import ZipFile
import io
import pandas as pd
import os
import numpy as np
from Bio.Seq import Seq


def grabZipCount(inputzip):
    dataStr = inputzip.split('/')[-1].split('.')[0] + "/fastqc_data.txt"
    with ZipFile(inputzip) as z:
        with z.open(dataStr) as f:
            qcData = io.TextIOWrapper(f, newline='\n')
            for line in qcData:
                if line.startswith('Total'):
                    return int(line.strip().split()[2])


def revC(string):
    revStr = ''.join(reversed(string))
    return str(Seq(revStr.complement()))


def parseSS(ss):
    ssdf = pd.read_csv(ss, comment='[')
    ssdf = ssdf.dropna()
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
