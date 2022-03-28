import configparser
from rich import print
import os
import glob
import psutil

def sambaDup():
    dupLis = glob.glob("./*markdup.txt")
    for sample in sorted(dupLis):
        name = sample.replace(".markdup.txt","")
        with open(sample) as f:
            for line in f:
                if 'mapped' in line.strip() and 'mate' not in line.strip():
                    mappedReads = int(line.strip().split(' ')[0])
                if 'duplicates' in line.strip():
                    dupReads = int(line.strip().split(' ')[0])
        rich.print("{} Mapped: {} Duplicates: {} percentage: {}".format(name, mappedReads, dupReads, (dupReads*100)/mappedReads))

def chModder(prefix):
    projList = glob.glob("Project_*")
    if len(projList) > 0:
        for proj in projList:
            # Skip PIs not from the institute.
            if len(proj.split('_')) == 4:
                PI = proj.split('_')[-1].lower()
                if PI == 'cabezas-wallscheid':
                    PI = 'cabezas'
                flowCell = os.path.abspath("./").split('/')[-1]
                if os.path.exists(os.path.join(prefix, PI, "sequencing_data",flowCell)):
                    clipPath = os.path.join(prefix, PI, "sequencing_data",flowCell)
                elif os.path.exists(os.path.join(prefix, PI, "sequencing_data2",flowCell)):
                    clipPath = os.path.join(prefix, PI, "sequencing_data2",flowCell)
                elif os.path.exists(os.path.join(prefix, PI, "sequencing_data3", flowCell)):
                    clipPath = os.path.join(prefix, PI, "sequencing_data3", flowCell)
                print(clipPath)
                for r, dirs, files in os.walk(clipPath):
                    for d in dirs:
                        if 'Analysis' not in os.path.join(r, d):
                            os.chmod(os.path.join(r, d), 0o750)
                    for f in files:
                        if 'Analysis' not in (os.path.join(r, f)):
                            os.chmod(os.path.join(r, f), 0o750)                
                rich.print("Released [bold green]{}[/bold green]".format(proj))
            else:
                rich.print("Skipped [bold green]{}[/bold green]".format(proj))
    else:
        rich.print("No Projects found.")
        

def projCP(destination):
    rich.print(
        "Shipping to [bold magenta]{}[/bold magenta]...".format(destination))
    for qc in glob.glob("Project_*/*multiqc_report.html"):
        des = os.path.join(destination, qc.split('/')[0] + '.html')
        subprocess.run(['cp', qc, des])
        rich.print("copied [bold green]{}[/bold green].".format(qc))
    subprocess.run(['cp', 'ContaminationReport.pdf', destination])
    rich.print("Shipped the contamination report.")


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
    # config can be either under user's home, home/.dotfiles, home/.dotfiles_WD
    _home = os.path.expanduser("~")
    _homeini = os.path.join(_home, 'wd40.ini')
    _dotini = os.path.join(_home, '.dotfiles', 'wd40.ini')
    _wddotini = os.path.join(_home,'.dotfiles_WD', 'wd40.ini')
    # Priority home > .dotfiles > .dotfiles_WD
    inilocs = [
        _homeini,
        _dotini,
        _wddotini
    ]
    for ini in inilocs:
        if os.path.exists(ini):
            config.read(ini)
            return config, os.path.abspath(ini)
    sys.exit("No config found! ~/wd40.ini, ~/.dotfiles/wd40.ini or ~/.dotfiles_WD/wd40.ini")

