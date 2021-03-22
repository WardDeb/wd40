import os
import subprocess
import glob
import rich


def fastQCrunner(fastQC, multiQC):
    projectDirs = glob.glob("Project*")
    for projectDir in projectDirs:
        QCpath = "FASTQC_" + projectDir
        if os.path.isdir("FASTQC_" + projectDir):
            rich.print(("{} already exists. "
                        "Please remove it yourself.").format(QCpath))
        else:
            os.mkdir("FASTQC_" + projectDir)
            samples = glob.glob(os.path.join(projectDir, "Sample*"))
            for sample in samples:
                fqFiles = [i for i in glob.glob(
                    os.path.join(
                        sample, "*fastq.gz")) if 'optical' not in i]
                QCout = "FASTQC_" + sample
                os.mkdir(QCout)
                fastQCcmd = [fastQC, "-t", "30", "-o", QCout] + fqFiles
                subprocess.run(fastQCcmd)
            if not os.path.exists(
                os.path.join(
                    projectDir,
                    'multiqc_report.html')):
                multiQCcmd = [multiQC, '-o', projectDir, QCpath]
                subprocess.run(multiQCcmd)
                os.remove(os.path.join(projectDir, 'multiqc_data'))
            else:
                rich.print("multiQC exists already. Carry on.")
