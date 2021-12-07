import argparse

parser = argparse.ArgumentParser(description='Grab motifs from ame tsv file and subset jaspar file according to it.')

parser.add_argument('-i', type=str, required=True, help='ame.tsv')
parser.add_argument('-j', type=str, required=True, help='jaspar.txt')
args = parser.parse_args()

catchMotfs = []
ameFiles = args.i.split(',')
for ame in ameFiles:
    with open(ame) as f:
        for line in f:
            if line.startswith('rank') or line.startswith('#'):
                continue
            elif line.strip() == '':
                break
            else:
                lin = line.strip().split()
                motif = lin[2]
                pval = float(lin[6])
                pwmMin = float(lin[12])
                if pval < 1e-10 and pwmMin > 10:
                    if motif not in catchMotfs:
                        catchMotfs.append(motif)

catchMotfs = set(catchMotfs)
catch = False
with open(args.j) as f:
    for line in f:
        if line.startswith('MOTIF'):
            mot = line.strip().replace('MOTIF ','')
            if mot in catchMotfs:
                catch = True
                print(line.strip())
            else:
                catch = False
        elif catch == True:
            print(line.strip())



