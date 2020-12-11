import configparser
import os
import psutil
import subprocess

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

