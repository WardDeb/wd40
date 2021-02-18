import os
import subprocess
import glob

def fastQCrunner(fastQC, multiQC):
    projectDirs = []
    for i in os.listdir():
        if 'Project_' in i and 'FASTQC' not in i:
            projectDirs.append(i)
            print("Project {} found.".format(i))
    for projectDir in projectDirs:
        QCpath = "FASTQC_" + projectDir
        if os.path.isdir(QCpath):
            print("{} already exists. Please remove it yourself.".format(QCpath))
        else:
            fqFiles = [i for i in glob.glob(projectDir + "/*/*fastq.gz") if 'optical' not in i]
            os.mkdir(QCpath)
            for item in fqFiles:
                print(item)
            fastQCcmd = [fastQC,"-t", "30", "-o",QCpath] + fqFiles
            print(' '.join(fastQCcmd))
            subprocess.run(fastQCcmd)
            #run multiQC
            if not os.path.exists(os.path.join(projectDir, 'multiqc_report.html')):
                multiQCcmd = [multiQC, '-o',projectDir, QCpath]
                subprocess.run(multiQCcmd)