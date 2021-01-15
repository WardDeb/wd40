import os
import subprocess
import matplotlib.pyplot as plt
import csv
import numpy as np

def fqscreentopng(fname):
    species=[]
    ohol=[]
    mhol=[]
    ohml=[]
    mhml=[]
    for line in csv.reader(open(fname, "r"), dialect="excel-tab") :
        if(len(line) == 0) :
            break
        if(line[0].startswith("#")) :
            continue
        if(line[0].startswith("Genome")) :
            continue
        species.append(line[0])
        ohol.append(float(line[5]))
        mhol.append(float(line[7]))
        ohml.append(float(line[9]))
        mhml.append(float(line[11]))

    ohol = np.array(ohol)
    mhol = np.array(mhol)
    ohml = np.array(ohml)
    mhml = np.array(mhml)

    ind = np.arange(len(species))
    p1 = plt.bar(ind, tuple(ohol), color="#0000FF")
    p2 = plt.bar(ind, tuple(mhol), color="#6699FF", bottom=tuple(ohol))
    p3 = plt.bar(ind, tuple(ohml), color="#FF0000", bottom=tuple(ohol+mhol))
    p4 = plt.bar(ind, tuple(mhml), color="#FF6699", bottom=tuple(ohol+mhol+ohml))

    plt.title("%s" % fname.replace("subsample_screen.txt","").split("/")[-1])
    plt.ylabel("%")
    plt.ylim((0,105))
    plt.xticks(ind, species, rotation="vertical")
    plt.yticks(np.arange(0,110,10))
    plt.legend((p4[0], p3[0], p2[0], p1[0]), ("repeat", "conserved", "multimap", "unique"))
    plt.tight_layout()
    plt.savefig("%s.png" % fname.replace(".subsample_screen.txt","_screen"))
    plt.close()

def screenRunner(fastq_screen,fastq_conf,seqtk):
    for directory in os.listdir():
        if 'Project' in directory and 'FASTQC' not in directory:
            for sample in os.listdir(directory):
                if 'Sample' in sample:
                    for fqfile in os.listdir(os.path.join(directory, sample)):
                        if 'fastq.gz' in fqfile and not 'optical' in fqfile and 'R2' in fqfile:
                            outPrefix = os.path.join(directory,sample)
                            outName = os.path.join(outPrefix, fqfile.replace("_R2.fastq.gz", ".subsample.fq"))
                            seqtkCMD = [seqtk, "sample", "-s", "123456", os.path.join(outPrefix,fqfile), "1000000"]
                            if not os.path.exists(os.path.join(outPrefix,fqfile)):
                                o = open(outName, 'w')
                                subprocess.run(seqtkCMD, stdout=o)
                                o.close()
                                print("ran seqtk on {} with {} as out.".format(fqfile, outName))
                            else:
                                print("subsampled fastq file for {} already exists.".format(fqfile))
                            # Run fastqscreen
                            if not os.path.exists(os.path.join(directory, sample, fqfile.replace("_R2.fastq.gz",".subsample_screen.txt"))):
                                os.chdir(os.path.join(directory, sample))
                                fqscreenCMD = [fastq_screen,"--conf",fastq_conf, "--threads", "40", "--quiet", "--aligner", "bowtie2", "--subset", "0", fqfile.replace("_R2.fastq.gz", ".subsample.fq")]
                                print("Running fqscreen with {}".format(" ".join(fqscreenCMD)))
                                subprocess.run(fqscreenCMD)
                                os.chdir("../../")
                            else:
                                print("fastqscreen for {} already ran.".format(fqfile))
                            if not os.path.exists(os.path.join(directory, sample, fqfile.replace("_R2.fastq.gz","_screen.png"))):
                                os.chdir(os.path.join(directory, sample))
                                fqscreentopng(fqfile.replace("_R2.fastq.gz",".subsample_screen.txt"))
                                os.chdir("../../")
                            else:
                                print("png already created.".format(fqfile))


                    