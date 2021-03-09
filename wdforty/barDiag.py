from Bio.Seq import Seq
import json
from zipfile import ZipFile
import io
import pandas as pd
import os
import numpy as np

def grabZipCount(inputzip):
    dataStr = inputzip.split('/')[-1].split('.')[0] + "/fastqc_data.txt"
    with ZipFile(inputzip) as z:
        with z.open(dataStr) as f:
            qcData = io.TextIOWrapper(f, newline='\n')
            for line in qcData:
                if line.startswith('Total'):
                    return int(line.strip().split()[2])


def rev(string):
    return ''.join(reversed(string))
# revp5 = str(Seq(rev(str(p5))).complement())
# Could include an automatic reverser or something.



def parseSS(ss):
    ssdf = pd.read_csv(ss, comment='[')
    ssdf = ssdf.dropna()
    # Fetch the total number of reads per sample
    readCount = []
    for index, row in ssdf.iterrows():
        projID = "Project_" + row['Sample_Project']
        sampleID = "Sample_" + row['Sample_ID']
        sampleName = row['Sample_Name']
        zipStr = os.path.join("FASTQC_" + projID, sampleID, sampleName + "_R1_fastqc.zip")
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
    UndComb = {}
    with open(statFile) as f:
        stats = json.load(f)
        candidates = {}
        for lane in stats['UnknownBarcodes']:
            for comb in lane['Barcodes']:
                if np.round(
                    depth/lane['Barcodes'][comb]
                ) == 1 or \
                depth < lane['Barcodes'][comb]:
                    if comb not in candidates:
                        candidates[comb] = lane['Barcodes'][comb]
        return candidates

            


# TODO This goes over the entire smaplesheet ,
# we can improve it by adding a specific project to through
# Also reversin i7, in case it ever needs to be rced.
# with open(args.i, "r") as f:
#    with open("SampleSheet_rc.csv", "w+") as out_f: #Add it to the arg
#        for index, line in enumerate(f):
#            if index <2:
#                out_f.write(line)
#            else:
#                line = line.split(",")
#                print(line)
#                if line[5].split("\n")[0] not in args.p:
#                    out_f.write("{},{},{},{},{},{}".format(line[0],line[1],line[2],line[3],line[4],line[5]))
#                else:
#                    print(line)
#                    out_f.write("{},{},{},{},".format(line[0],line[1],line[2],line[3]))
#                    i5 = Seq(line[4], generic_dna).reverse_complement()
#                    out_f.write("{},{}".format(str(i5),line[5]))
