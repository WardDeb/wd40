#!/usr/bin/env python3
import argparse
import wdforty.misc
import wdforty.catRun
import wdforty.barDiag
import wdforty.QC
import wdforty.Clump
import wdforty.QCScreen
import wdforty.specScreen
import sys

def main():
    parser = argparse.ArgumentParser(description='Here to make your life easy! fac.py <command> [<args>]')

    parser.add_argument('command', type=str, choices = ['barDiag','bigClump','catRun', 'projCP', 'storageHammer','specScreen', 'QC', 'QCScreen'],
                        help='Give the command you would like to perform. ')
    parser.add_argument('--projects', 
                        help='catRun: list the projects you would like to combine. Seperated by comma! e.g. Project_1111')
    parser.add_argument('--flowcells',
                        help='catRun: list the flowcells (looked for under baseDir specified in ini) where the projects reside.')
    parser.add_argument('--specList',
                        help='Provide a TSV file that contains a project ID (e.g. Project_1111), followed by a PI id.')
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

    if args.command == 'specScreen':
        projPIdic = {}
        try:
            with open('args.specList') as f:
                for line in f:
                    proj = line.strip().split()[0]
                    PI = line.strip().split()[1]
                    projPIdic[proj] = PI
        except:
            print('Error parsing the specList. Please reformat.')
        # LINK.
        # SnakePipes.
        # retain the featurecounts file.

        

if __name__ == "__main__":
    main()