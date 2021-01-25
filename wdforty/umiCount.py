import os
import subprocess
from Bio import SeqIO
import gzip

def umiCounter(umi, fqFile):
    countDic = {}
    projectDirs = []
    for i in os.listdir():
        if 'Project_' in i and 'FASTQC' not in i:
            projectDirs.append(i)
            countDic[i] = {}
    for proj in projectDirs:
        for sample in os.listdir(proj):
            if 'Sample' in sample:
                for fq in os.listdir(os.path.join(proj, sample)):
                    if fqFile+".fastq.gz" in fq and 'optical' not in fq:
                        umiCount = 0
                        with gzip.open(os.path.join(proj, sample, fq),"rt") as handle:
                            recs = SeqIO.parse(handle,"fastq")
                            for seq in recs:
                                if umi in seq.seq:
                                    umiCount += 1
                        print("{} {} : {}".format(proj, fq, umiCount))
                        countDic[proj][sample] = umiCount
    return countDic