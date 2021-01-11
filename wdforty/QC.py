import os
import subprocess

def fastQCrunner(fastQC, multiQC):
    for i in os.listdir():
        if 'Project_' in i and 'FASTQC' not in i:
            projectDir = i
    if not projectDir:
        print("Can't find a project directory.")
    QCpath = "FASTQC_" + projectDir
    if os.path.isdir(QCpath):
        print("{} already exists. Please remove it yourself.".format(QCpath))
    else:
        sampleNames = []
        for i in os.listdir(projectDir):
            if 'Sample' in i:
                sampleNames.append(i)
        os.mkdir(QCpath)
        for sample in sampleNames:
            fastQCout = os.path.join(QCpath, sample)
            readFiles = []
            for i in os.listdir(os.path.join(projectDir, sample)):
                if 'fastq.gz' in i and 'optical' not in i:
                    readFiles.append(os.path.join(projectDir, sample, i))         
            os.mkdir(fastQCout)
            fastQCcmd = [fastQC,"-t", "20", "-o",fastQCout,readFiles[0],readFiles[1]]
            print(' '.join(fastQCcmd))
            print(readFiles)
            subprocess.run(fastQCcmd)
        #run multiQC
        multiQCcmd = [multiQC, '-o',projectDir, QCpath]


