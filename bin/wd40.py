#!/usr/bin/env python3
import argparse
import wdforty.misc
import wdforty.catRun
import wdforty.barDiag
import wdforty.QC
import wdforty.Clump
import wdforty.QCScreen
import wdforty.umiCount
import sys

def main():
    parser = argparse.ArgumentParser(description='Here to make your life easy! fac.py <command> [<args>]')

    parser.add_argument('command', type=str, choices = ['barDiag', 'bigClump', 'catRun', 'projCP', 'storageHammer',
     'QC', 'QCScreen', 'umiCount', 'linkscReads'],
                        help='Give the command you would like to perform. ')
    parser.add_argument('--projects', 
                        help='catRun: list the projects you would like to combine. Seperated by comma! e.g. Project_1111')
    parser.add_argument('--flowcells',
                        help='catRun: list the flowcells (looked for under baseDir specified in ini) where the projects reside.')
    parser.add_argument('--specList',
                        help='Provide a TSV file that contains a project ID (e.g. Project_1111), followed by a PI id.')
    parser.add_argument('--umi',
                        help='provide the UMI sequence to screen for.')
    parser.add_argument('--umiFqFile', choices = ["R1", "R2"],
                        help='Specify if the UMI should be searched for in R1 or R2')
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
        #print(ssDic)
        UndComb = wdforty.barDiag.parseUnd()
        #print(UndComb)
        revSS = wdforty.barDiag.revP5('SampleSheet.csv')
        for i in revSS:
            print(','.join(i))

    if args.command == 'bigClump':
        wdforty.Clump.clumpRunner(config['QC']['clumpifyPath'], config['QC']['splitFQPath'])

    if args.command == 'QC':
        fastQC = config['QC']['fastQCPath']
        multiQC = config['QC']['multiQCPath']
        wdforty.QC.fastQCrunner(fastQC, multiQC)

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
        if not args.projects:
            print("Specify a project directory.")
            sys.exit()
        else:
            wdforty.misc.scLinker(args.projects)

if __name__ == "__main__":
    main()