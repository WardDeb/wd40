import os
import subprocess

def fastQCrunner(fastQC, multiQC):
    projectDirs = []
    for i in os.listdir():
        if 'Project_' in i and 'FASTQC' not in i:
            projectDirs.append(i)
    if len(projectDirs) == 0:
        print('I could not find any project directories.')
    else:
        print("Can't find a project directory.")
    for projectDir in projectDirs:
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
                subprocess.run(fastQCcmd)
            #run multiQC
        if not os.path.exists(os.path.join(projectDir, 'multiqc_report.html')):
            multiQCcmd = [multiQC, '-o',projectDir, QCpath]
            subprocess.run(multiQCcmd)


