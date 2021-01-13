import os
import subprocess

def clumpRunner(clumploc,splitFQ):
    for directory in os.listdir():
        if 'Project' in directory and 'FASTQC' not in directory:
            for sample in os.listdir(directory):
                if 'Sample' in sample:
                    fqfiles = []
                    if not any('optical' in i for i in os.listdir(os.path.join(directory, sample))) and not any('temp' in i for i in os.listdir(os.path.join(directory,sample))):
                        for fqfile in os.listdir(os.path.join(directory, sample)):
                            if 'fastq.gz' in fqfile:
                                fqfiles.append(fqfile)
                    if len(fqfiles) == 2:
                        out = 'out=' + os.path.join(directory,sample,'temp.fq.gz')
                        R1 = 'in=' + os.path.join(directory,sample,fqfiles[0])
                        R2 = 'in2=' + os.path.join(directory,sample,fqfiles[1])
                        clumpCmd = [clumploc, 'dupesubs=0', 'qin=33', 'markduplicates=t', 'optical=t', 'dupedist=12000', '-Xmx220G', 'threads=20', R1, R2, out]
                        print(clumpCmd)
                        subprocess.run(clumpCmd)
                        for i in fqfiles:
                            if 'R1.fastq.gz' in i:
                                os.chdir(os.path.join(directory, sample))
                                splitCmd = [splitFQ,'temp.fq.gz','1',i.replace("_R1.fastq.gz",""), '20']
                                print(splitCmd)
                                subprocess.run(splitCmd)
                                os.remove('temp.fq.gz')
                                os.chdir('../../')
                    elif len(fqfiles) == 1:
                        print("Add single end code here.")