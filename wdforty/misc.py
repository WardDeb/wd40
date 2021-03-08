import configparser
import os
import psutil
import subprocess
import glob
import rich


def projCP(destination):
    rich.print(
        "Shipping to [bold magenta]{}[/bold magenta]...".format(destination))
    for qc in glob.glob("Project_*/*multiqc_report.html"):
        des = os.path.join(destination, qc.split('/')[0] + '.html')
        subprocess.run(['cp', qc, des])
        rich.print("copied [bold green]{}[/bold green].".format(qc))
    subprocess.run(['cp', 'ContaminationReport.pdf', destination])
    rich.print("Shipped the contamination report.")


def storageHammer(PIs, prefix, postfix):
    for pi in PIs:
        seqDat = os.path.join(prefix, pi, postfix)
        if os.path.exists(seqDat):
            if os.path.exists(os.path.join(prefix, pi, postfix + "2")):
                seqDat = os.path.join(prefix, pi, postfix + "2")
            hdd = psutil.disk_usage(seqDat)
            if hdd.used/hdd.total > 0.90:
                rich.print(
                    ("[bold red]{}'s sequencing data folder is above 90%! "
                     "Space Free: {} "
                     "GB[/bold red]").format(pi, hdd.free // (2**30)))
            if hdd.used/hdd.total < 0.90 and hdd.used/hdd.total > 0.80:
                rich.print(
                    ("[bold cyan]{}'s sequencing data folder is above 80%. "
                     "Space Free: {} "
                     "GB[/bold cyan]").format(pi, hdd.free // (2**30)))
        else:
            procDat = os.path.join(prefix, pi)
            hdd = psutil.disk_usage(procDat)
            if hdd.used/hdd.total > 0.90:
                if 'processing' in pi:
                    rich.print(
                        ("[bold red]{} processing volume is above 90%! "
                         "Space Free: {} "
                         "GB[/bold red]").format(pi, hdd.free // (2**30)))
                else:
                    rich.print(
                        ("[bold red]{} is above 90%! "
                         "Space Free: {} "
                         "GB[/bold red]").format(procDat, hdd.free // (2**30)))


def scLinker(projectDir):
    files = glob.glob(
        os.path.join(
            os.path.abspath(
                projectDir), "Sample_*", "*_R1.fastq.gz"))
    print(files)
    samples = {}
    for sample in files:
        bname = os.path.basename(sample)[:-12]
        pname = bname[:-2]
        os.makedirs(os.path.join("fastq", pname), exist_ok=True)
        if pname not in samples:
            samples[pname] = []
        samples[pname].append(bname)
        R1 = "{}_S1_L001_R1_001.fastq.gz".format(
            os.path.join(
                "fastq", pname, bname))
        R2 = "{}_S1_L001_R2_001.fastq.gz".format(
            os.path.join(
                "fastq", pname, bname))
        if not os.path.exists(R1):
            os.symlink(sample, R1)
        if not os.path.exists(R2):
            os.symlink("{}_R2.fastq.gz".format(sample[:-12]), R2)
        print("Relinked {}".format(sample))


def fastQC(projectDir):
    for sample in os.listdir(projectDir):
        print(sample)


def getConfig():
    config = configparser.ConfigParser()
    config.read("%s/wd40.ini" % os.path.expanduser("~"))
    return config
