import os
import subprocess

def clumpRunner(clumploc,splitFQ):
    for directory in os.listdir():
        if 'Project' in directory and 'FASTQC' not in directory:
            for sample in os.listdir(directory):
                if 'Sample' in sample:
                    fqfiles = []
                    for fqfile in os.listdir(os.path.join(directory, sample)):
                        if 'fastq.gz' in fqfile and not 'optical' in fqfile:
                            fqfiles.append(fqfile)
                    if len(fqfiles) == 2:
                        out = 'out=' + os.path.join(directory,sample,'temp.fq.gz')
                        R1 = 'in=' + os.path.join(directory,sample,fqfiles[0])
                        R2 = 'in2=' + os.path.join(directory,sample,fqfiles[1])
                        clumpCmd = [clumploc, 'dupesubs=0', 'qin=33', 'markduplicates=t', 'optical=t', 'dupedist=12000', '-Xmx220G', 'threads=20', R1, R2, out]
                        if not os.path.isfile(os.path.join(directory,sample,'temp.fq.gz')):
                            subprocess.run(clumpCmd)
                        for i in fqfiles:
                            print(i)
                            if 'R1.fastq.gz' in i:
                                os.chdir(os.path.join(directory, sample))
                                splitCmd = [splitFQ,'temp.fq.gz','1',i.replace("_R1.fastq.gz",""), '20']
                                if not os.path.isfile('ClumpSplit.done'):
                                    subprocess.run(splitCmd)
                                    os.remove('temp.fq.gz')
                                    open('ClumpSplit.done', 'w')
                                os.chdir('../../')
                    elif len(fqfiles) == 1:
                        print("Add single end code here.")