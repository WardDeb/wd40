#!/usr/bin/env python3
import argparse
import wdforty.misc
import wdforty.catRun
import wdforty.barDiag
import wdforty.QC
import wdforty.Clump
import wdforty.QCScreen
import wdforty.umiCount
import rich
import sys


def main():
    # Main args.
    parser = argparse.ArgumentParser(
        description='Facilitate seq processing! fac.py <command> [<args>]'
    )
    parser.add_argument(
        'command',
        type=str,
        choices=['barDiag',
                 'bigClump',
                 'catRun',
                 'projCP',
                 'storageHammer',
                 'QC',
                 'QCScreen',
                 'umiCount',
                 'linkscReads'],
        help='Give the command you would like to perform. ')
    try:
        options = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)
    
    #Read config.
    config = wdforty.misc.getConfig()

    if args.command == 'projCP':
        print("projCP")
        #wdforty.misc.projCP(config['projCP']['destination'])

    if args.command == 'storageHammer':
        PIs = config['storageHammer']['PIs'].split(',')
        prefix = config['storageHammer']['prefix']
        postfix = config['storageHammer']['postfix']
        wdforty.misc.storageHammer(PIs, prefix, postfix)

    if args.command == 'catRun':
        print("doing the CAT")
        #try:
        #    Projects = args.projects.replace(' ','').split(',')
        #except:
        #    print("catRun module requires projects specified with --project Proj1,Proj2")
        #    sys.exit()
        #try:
        #    Flowcells = args.flowcells.replace(' ','').split(',')   
        #except:
        #    print("catRun module requires flowcells specified with --flowcells flow1,flow2")
        #    sys.exit()
        #baseDir = config['catRun']['baseDir']
        #wdforty.catRun.catRun(Projects, Flowcells, baseDir)

    if args.command == 'barDiag':
        print("diagnosing some barcodes.")
        #ssDic = wdforty.barDiag.parseSS('SampleSheet.csv')
        #print(ssDic)
        #UndComb = wdforty.barDiag.parseUnd()
        #print(UndComb)
        #revSS = wdforty.barDiag.revP5('SampleSheet.csv')
        #for i in revSS:
        #    print(','.join(i))

    if args.command == 'bigClump':
        print("Hammerclumps. Sit tight, this takes a while.")
        #wdforty.Clump.clumpRunner(config['QC']['clumpifyPath'], config['QC']['splitFQPath'])

    if args.command == 'QC':
        print("Running fastqc&multiqc")
        #fastQC = config['QC']['fastQCPath']
        #multiQC = config['QC']['multiQCPath']
        #wdforty.QC.fastQCrunner(fastQC, multiQC)

    if args.command == 'QCScreen':
        fastqScreen = config['QC']['fqScreenPath']
        seqtk = config['QC']['seqtkPath']
        screenconf = config['QC']['fqScreenConf']
        wdforty.QCScreen.screenRunner(fastqScreen,screenconf, seqtk)
    
    if args.command == 'umiCount':
        if not args.umiFqFile:
            print("Specify --umiFqFile (R1 or R2)")
            sys.exit()
        elif not args.umi:
            print("Specify --umi SEQUENCE")
            sys.exit()
        else:
            resDic = wdforty.umiCount.umiCounter(args.umi, args.umiFqFile)
            print(resDic)

    if args.command == 'linkscReads':
        print("Linking some fqs inside 'fqs' dir.")
        #if not args.projects:
        #    print("Specify a project directory.")
        #    sys.exit()
        #else:
        #    wdforty.misc.scLinker(args.projects)

if __name__ == "__main__":
    main()