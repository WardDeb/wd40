import os
import argparse

parser = argparse.ArgumentParser(description='rename a bunch of fastq files.')

parser.add_argument('-i', type=str, required=True, help='txt file with source\ttarget.')

args = parser.parse_args()

renameDic = {}
with open(args.i) as f:
    for line in f:
        source = line.strip().split()[0]
        target = line.strip().split()[1]
        renameDic[source] = target
for source in renameDic:
    R1 = source + '_R1.fastq.gz'
    R2 = source + '_R2.fastq.gz'
    R1stat = False
    R2stat = False
    if not os.path.exists(R1):
        print("{} not found...".format(R1))
    else:
        os.rename(R1, renameDic[source] + '_R1.fastq.gz')
        R1stat = True
    if not os.path.exists(R2):
        print("{} not found...".format(R2))
    else:
        os.rename(R2, renameDic[source] + '_R2.fastq.gz')
        R2stat = True
    if R1stat and R2stat:
        print("Renamed {} in to {} for both R1 and R2.".format(source, renameDic[source]))

