from rich import print, inspect
from rich.console import Console
from rich.table import Table
from wdforty.misc import getConfig
import glob
import os
import psutil


def dsk():
    print("Running diskCheck...")
    conf, confPath = getConfig()
    print('Config read from {}'.format(confPath))
    PIs = conf['internals']['PIs'].split(',')
    prefix = conf['internals']['pref']
    grps = conf['internals']['grpMatch'].split(',')
    # build glob list
    glbDir = []
    for pi in PIs:
        for piDir in glob.glob(
            os.path.join(prefix, pi, '*')
        ):
            glbDir.append(piDir)
    for grp in grps:
        for grpDir in glob.glob(
            os.path.join(prefix, grp + '*')
        ):
            glbDir.append(grpDir)
    checkSpace(glbDir)


def checkSpace(glbDir):
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Dir")
    table.add_column("% occupied")
    table.add_column("GB free")
    badCount = 0
    for dir in sorted(glbDir):
        hdd = psutil.disk_usage(dir)
        gbFree = round(hdd.free // (2**30), 2)
        if hdd.used/hdd.total > 0.9:
            badCount += 1
            table.add_row(
                dir,
                str(round(hdd.used/hdd.total * 100, 2)),
                str(gbFree)
            )
    if badCount:
        console.print(table)
    else:
        print("[bold green] No disks occupied > 90%.")

