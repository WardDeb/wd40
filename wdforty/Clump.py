import os
import subprocess
import glob
import rich
import sys


def clumpRunner(clumploc, splitFQ, machine='Nova'):
    projects = glob.glob("Project*")
    print("Found {} Projects.".format(len(projects)))
    for project in projects:
        if not glob.glob(os.path.join(project, "Sample*/*optical*")):
            rich.print(
                "{} No optical duplicated fastqs. Invoking.".format(project))
            #clumpify_NextSeq_options=spany=t adjacent=t
            samples = glob.glob(os.path.join(project, "Sample*"))
            for sample in samples:
                fqFiles = glob.glob(os.path.join(sample, "*fastq.gz"))
                if len(fqFiles) == 1:
                    out = 'out=' + os.path.join(sample, 'temp.fq.gz')
                    R1 = 'in=' + sorted(fqFiles)[0]
                    if machine == 'Nova':
                        clumpCmd = [
                            clumploc,
                            'dupesubs=0',
                            'qin=33',
                            'markduplicates=t',
                            'dupedist=12000',
                            '-Xmx220G',
                            'threads=20',
                            R1,
                            out
                        ]
                        fqBase = sorted(
                            fqFiles
                            )[0].split('/')[-1].replace("_R1.fastq.gz", "")
                        splitCmd =  splitCmd = [splitFQ, 'temp.fq.gz', '0', fqBase, '20']
                    elif machine == 'nextSeq':
                        clumpCmd = [
                            clumploc,
                            'dupesubs=0',
                            'qin=33',
                            'markduplicates=t',
                            'optical=t',
                            '-Xmx220G',
                            'threads=20',
                            'spany=t',
                            'adjacent=t',
                            'dupedist=40',
                            R1,
                            out
                        ]
                        fqBase = sorted(
                            fqFiles
                            )[0].split('/')[-1].replace("_R1.fastq.gz", "")
                        splitCmd =  splitCmd = [splitFQ, 'temp.fq.gz', '0', fqBase, '20']
                    print(' '.join(clumpCmd))
                    subprocess.run(clumpCmd)
                    os.chdir(sample)
                    print(' '.join(splitCmd))
                    subprocess.run(splitCmd)
                    os.chdir('../../')
                elif len(fqFiles) == 2:
                    out = 'out=' + os.path.join(sample, 'temp.fq.gz')
                    R1 = 'in=' + sorted(fqFiles)[0]
                    R2 = 'in2=' + sorted(fqFiles)[1]
                    clumpCmd = [clumploc,
                                'dupesubs=0',
                                'qin=33',
                                'markduplicates=t',
                                'optical=t',
                                'dupedist=12000',
                                '-Xmx220G',
                                'threads=20',
                                R1,
                                R2,
                                out]
                    fqBase = sorted(
                        fqFiles
                        )[0].split('/')[-1].replace("_R1.fastq.gz", "")
                    splitCmd = [splitFQ, 'temp.fq.gz', '1', fqBase, '20']
                    print(' '.join(splitCmd))
                    subprocess.run(clumpCmd)
                    os.chdir(sample)
                    subprocess.run(splitCmd)
                    os.chdir('../../')
                else:
                    print('noClump support for >2 fastq files per sample.')
                    sys.exit()
