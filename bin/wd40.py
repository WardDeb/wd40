#!/usr/bin/env python3
import argparse
import wdforty.misc
import wdforty.catRun
import wdforty.barDiag
import wdforty.QC
import sys

parser = argparse.ArgumentParser(description='Here to make your life easy! fac.py <command> [<args>]')

parser.add_argument('command', type=str, choices = ['barDiag','catRun', 'projCP', 'storageHammer', 'QC'],
                    help='Give the command you would like to perform. ')
parser.add_argument('--projects', 
                    help='catRun: list the projects you would like to combine. Seperated by comma!')
parser.add_argument('--flowcells',
                    help='catRun: list the flowcells (looked for under baseDir specified in ini) where the projects reside.')
args = parser.parse_args()

config = wdforty.misc.getConfig()
if args.command == 'projCP':
    wdforty.misc.projCP(config['projCP']['destination'])

if args.command == 'storageHammer':
    PIs = config['storageHammer']['PIs'].split(',')
    prefix = config['storageHammer']['prefix']
    postfix = config['storageHammer']['postfix']
    wdforty.misc.storageHammer(PIs, prefix, postfix)

if args.command == 'catRun':
    try:
        Projects = args.projects.replace(' ','').split(',')
    except:
        print("catRun module requires projects specified with --project Proj1,Proj2")
        sys.exit()
    try:
        Flowcells = args.flowcells.replace(' ','').split(',')   
    except:
        print("catRun module requires flowcells specified with --flowcells flow1,flow2")
        sys.exit()
    baseDir = config['catRun']['baseDir']
    wdforty.catRun.catRun(Projects, Flowcells, baseDir)

if args.command == 'barDiag':
    ssDic = wdforty.barDiag.parseSS('SampleSheet.csv')
    print(ssDic)
    UndComb = wdforty.barDiag.parseUnd()
    print(UndComb)

if args.command == 'QC':
    fastQC = config['QC']['fastQCPath']
    multiQC = config['QC']['multiQCPath']
    wdforty.QC.fastQCrunner(fastQC, multiQC)
