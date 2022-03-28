import os
import sys
import glob
from pathlib import Path
from rich import print
from wdforty.misc import getConfig

def fetchLatestSeqDir(pref, PI, postfix):
    globStr = os.path.join(
        pref,
        PI,
        postfix + '*'
    )
    if len(glob.glob(globStr)) == 1:
        return glob.glob(globStr)[0]
    else:
        maxFolder = 0
        for seqDir in glob.glob(
            os.path.join(
                pref,
                PI,
                postfix + '*'
            )
        ):
            try:
                seqInt = int(seqDir[-1])
            except ValueError:
                seqInt = 0
                continue
            if seqInt > maxFolder:
                maxFolder = seqInt
        return(os.path.join(
            pref,
            PI,
            postfix + str(maxFolder)
        ))

def fetchFolders(flowcellPath, conf):
    institute_PIs = [i.lower() for i in conf['rel']['PIs'].split(',')]
    flowcellPath = os.path.abspath(flowcellPath)
    FID = flowcellPath.split('/')[-1]
    pref = conf['rel']['pref']
    post = conf['rel']['postfix']
    projDic = {}
    try:
        int(FID[:6])
        print("[green]Valid flowcell folder.[/green]")
    except ValueError:
        sys.exit("First 6 digits of flowcellpath don't convert to an int. Exiting.")
    for projF in glob.glob(
        os.path.join(
            flowcellPath,
            'Project_*'
        )
    ):
        proj = projF.split('/')[-1]
        PI = proj.split("_")[-1].lower()
        if PI == 'cabezas-wallscheid':
            PI = 'cabezas'
        if PI in institute_PIs:
            seqFolder = fetchLatestSeqDir(pref, PI, post)
            if os.path.exists(
                os.path.join(seqFolder, FID)
            ):
                projDic[proj] = [
                    PI + 'grp',
                    [
                        os.path.join(seqFolder, FID),
                        os.path.join(seqFolder, FID, proj),
                        os.path.join(seqFolder, FID, 'FASTQC_' + proj),
                        os.path.join(seqFolder, FID, 'Analysis_' + proj.replace('Project_', ''))
                    ]
                ]
            else:
                print("[red]{} not found! Double check[/red]".format(os.path.join(seqFolder, FID)))
        else:
            print("[bold cyan]Ignoring {}.[/bold cyan]".format(proj))
    return projDic

def releaser(F):
    for r, dirs, files in os.walk(F):
        for d in dirs:
            os.chmod(
                os.path.join(r, d),
                0o750
            )
        for f in files:
            fil = os.path.join(r, f)
            if not os.path.islink(fil):
                os.chmod(
                    fil,
                    0o750
                )

def folderRulings(grp, lis):
    flowcellF = lis[0]
    projectF = lis[1]
    fastqcF = lis[2]
    analysisF = lis[3]
    # flowcellF
    gotgrp = Path(flowcellF).group()
    if grp != gotgrp:
        print("[bold red]wrong grp for {}! change this manually.[/bold red]!")
    os.chmod(flowcellF, 0o750)
    releaser(projectF)
    releaser(fastqcF)
    if os.path.exists(analysisF):
        releaser(analysisF)

def rel(args):
    conf, confPath = getConfig()
    projDic = fetchFolders(args.flowcellPath, conf)
    for proj in projDic:
        '''
        every projDic[proj] is a nested list of:
        [grp, [flowcell, project, fastqc]]
        '''
        folderRulings(projDic[proj][0], projDic[proj][1])
        print(":thumbs_up:[bold green]Released {}[/bold green]".format(proj))