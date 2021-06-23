import argparse
import os
import subprocess
import glob
from multiprocessing import Pool

def grabber(acc, outName):
    # Fetch
    fetchCMD = ['prefetch',acc]
    print(
        "Fetching {}".format(acc)
    )
    subprocess.run(fetchCMD)
    # Ship
    os.rename(os.path.join(acc, acc + '.sra'), acc + '.sra')
    os.rmdir(acc)
    # Dump
    dumpCMD = ['fastq-dump','--split-3', acc + '.sra']
    print(
        "Dumping {}".format(acc)
    )
    subprocess.run(dumpCMD)
    # Ship and compress.
    os.remove(acc + '.sra')
    # Iterate over all fastqs.
    for read in glob.glob(acc + "*fastq"):
        compCMD = ['pigz', '-p', '20', read]
        subprocess.run(compCMD)
        inputstr = read + '.gz'
        targetstr = inputstr.replace(acc, outName)
        print("renaming {} into {}".format(inputstr, targetstr))
        os.rename(inputstr, targetstr)


def main():
    parser = argparse.ArgumentParser(
        prog='fetch some SRA accessions.',
        description='Download sra object, convert to fastq, rename and compress.',
        )

    # In and Output
    IO = parser.add_argument_group('Input/Output')
    IO.add_argument('-i', type=str, required=True,
                help='Give an input txt file containing SRA accession + final name.')
    
    args = parser.parse_args()

    sra = []
    outName = []
    with open(args.i) as f:
        for line in f:
            sra.append(line.strip().split()[0])
            outName.append(line.strip().split()[1])
    processPool = Pool(5)
    combinations = list(zip(sra, outName))
    processPool.starmap(grabber, combinations)

if __name__ == "__main__":
    main()
