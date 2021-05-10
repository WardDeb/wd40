import argparse

parser = argparse.ArgumentParser(description='read fimo tsv file and create BED file centered around regions.')

parser.add_argument('-i', type=str, required=True, help='input fimo TSV.')
args = parser.parse_args()

with open(args.i) as fimoOut:
    bedFormat = []
    for line in fimoOut:
        if not line.startswith('motif') and not line.startswith('#') and len(line.strip().split()) > 0:
            pval = float(line.strip().split()[7])
            qval = float(line.strip().split()[8])
            if pval < 0.05 and qval < 0.05:
                seqName = line.strip().split()[2]
                seqStart = int(seqName.split('_')[1])
                seqStop = int(seqName.split('_')[2])
                chrStr = seqName.split('_')[0]
                motStart = int(line.strip().split()[3])
                motStop = int(line.strip().split()[4])
                bedFormat.append([str(chrStr), str((seqStart+motStart)-10 ),str((seqStart+motStop) + 10)])

for i in bedFormat:
    print("{}\t{}\t{}".format(i[0],i[1],i[2]))
