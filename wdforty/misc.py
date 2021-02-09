import configparser
import os
import psutil
import subprocess
import glob

def scLinker(projectDir):
    files = glob.glob(os.path.join(os.path.abspath(projectDir),"Sample_*", "*_R1.fastq.gz"))
    print(files)
    samples = {}
    for sample in files:
        bname = os.path.basename(sample)[:-12]
        pname = bname[:-2]
        os.makedirs(os.path.join("fastq", pname), exist_ok=True)
        if pname not in samples:
            samples[pname] = []
        samples[pname].append(bname)
        R1 = "{}_S1_L001_R1_001.fastq.gz".format(os.path.join("fastq", pname, bname))
        R2 = "{}_S1_L001_R2_001.fastq.gz".format(os.path.join("fastq", pname, bname))
        if not os.path.exists(R1):
            os.symlink(sample, R1)
        if not os.path.exists(R2):
            os.symlink("{}_R2.fastq.gz".format(sample[:-12]), R2)
        print("Relinked {}".format(sample))

def fastQC(projectDir):
    for sample in os.listdir(projectDir):
       print(sample)

def projCP(destination):
    projDirs = []
    for i in os.listdir():
        if 'Project_' in i and 'FASTQC' not in i:
            projDirs.append(i)
    for i in projDirs:
        qcstr = os.path.join(i, 'multiqc_report.html')
        targetstr = os.path.join(destination, i +'.html')
        try:
            subprocess.run(['cp',qcstr,targetstr])
            print("Ran {}".format(qcstr))
        except:
            print("Couldn't find {}.".format(qcstr))
            continue
    try:
        subprocess.run(['cp','ContaminationReport.pdf', destination])
    except:
        print("Couldn't find the Contaminationreport.")

def getConfig() :
    config = configparser.ConfigParser()
    config.read("%s/wd40.ini" % os.path.expanduser("~"))
    return config

def storageHammer(PIs, prefix, postfix):
    for pi in PIs:
        seqDat = os.path.join(prefix,pi,postfix)
        if os.path.exists(seqDat):
            if os.path.exists(os.path.join(prefix,pi,postfix + "2")):
                seqDat = os.path.join(prefix,pi,postfix + "2")
            hdd = psutil.disk_usage(seqDat)
            if hdd.used/hdd.total > 0.90:
                print("{}'s sequencing data folder is above 90%! Space Free: {} GB".format(pi,hdd.free // (2**30)))
            if hdd.used/hdd.total < 0.90 and hdd.used/hdd.total > 0.80:
                print("{}'s sequencing data folder is above 80%. Space Free: {} GB".format(pi,hdd.free // (2**30)))
        else:
            procDat = os.path.join(prefix,pi)
            hdd = psutil.disk_usage(procDat)
            if hdd.used/hdd.total > 0.90:
                if 'processing' in pi:
                    print("{} processing volume is above 90%! Space Free: {} GB".format(pi,hdd.free // (2**30)))
                else:
                    print("{} is above 90%! Space Free: {} GB".format(procDat,hdd.free // (2**30)))

