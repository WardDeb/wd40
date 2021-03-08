import os
import subprocess
import glob
from rich.console import Console
import rich
import sys

def clumpRunner(clumploc,splitFQ):
    projects = glob.glob("Project*")
    print("Found {} Projects.".format(len(projects)))
    for project in projects:
        if not glob.glob(os.path.join(project, "Sample*/*optical*")):
            rich.print("{} doesn't have optical duplicated fastqs. Invoking.".format(project))
            samples = glob.glob(os.path.join(project, "Sample*"))
            for sample in samples:
                fqFiles = glob.glob(os.path.join(sample, "*fastq.gz"))
                if len(fqFiles) != 2:
                    rich.print("Only do this for paired end. exiting.")
                    sys.exit()
                else:
                    out = 'out=' + os.path.join(sample, 'temp.fq.gz')
                    R1 = 'in=' + sorted(fqFiles)[0]
                    R2 = 'in2=' + sorted(fqFiles)[1]
                    clumpCmd = [clumploc, 'dupesubs=0', 'qin=33',
                                'markduplicates=t', 'optical=t', 'dupedist=12000', '-Xmx220G', 'threads=20', R1, R2, out]
                    fqBase = sorted(fqFiles)[0].split('/')[-1].replace("_R1.fastq.gz", "")
                    splitCmd = [splitFQ, 'temp.fq.gz', '1', fqBase, '20']
                    console = Console()
                    print(' '.join(splitCmd))
                    subprocess.run(clumpCmd)
                    os.chdir(sample)
                    subprocess.run(splitCmd)
                    os.chdir('../../')