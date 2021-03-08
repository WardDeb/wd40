#!/usr/bin/env python3
import argparse
import textwrap
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
    config = wdforty.misc.getConfig()
    arguments_info = {
        "noArgs":{
            "barDiag":"Diagnose some common mistakes in sampleSheet file. Parses the Stats folder from bcl2fastq and sampleSheet.csv. Run from a flowcell folder.",
            "bigClump":"Run clumpify.sh serially, in case your fastq files are huge.",
            "projCP":"Copy over multiQC's and Contamination report to a more convenient location (defined in wd40.ini).",
            "storHam":"Iterate over processing volumes / PI folders and list those that are nearly full. (locations defined in wd40.ini).",
            "FastQC":"Run FastQC and subsequently multiQC from a flowcell folder. Handy if you generated these with catRun.",
            "QCScreen":"Run fastq_screen on a flowcell folder."
        },
        "Args":{
            "catRun":"Cat together samples (R1 and R2) from multiple flowcells.",
            "umiCount":"Run umi demux. Specify project dir.",
            "linkSCReads":"link fastqfiles using the cellranger nomenclature."
        }
    }
    parser = argparse.ArgumentParser("wd40.py", usage=argparse.SUPPRESS)
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
        help=argparse.SUPPRESS)
    parser.formatter_class = lambda prog: argparse.RawDescriptionHelpFormatter(prog, max_help_position=25, width=90)
    parser.description = textwrap.dedent('''
                wd40.py - Universal lubricant.

                Usage: wd40.py [command]

                ''')

    for argTyp in arguments_info:
        if argTyp == 'noArgs':
            parser.description += "Commands without arguments (runs from workDir):\n"
        elif argTyp == 'Args':
            parser.description += "Commands requiring arguments:\n"
        for comm in arguments_info[argTyp]:
            parser.description += "    {}\t\t{}\n".format(comm, arguments_info[argTyp][comm])
    parser.description += "\n"

    if len(sys.argv[1:]) == 0:
        parser.print_help()
        sys.exit()

    args = parser.parse_args()
    print(args.command)
    
    # Main args.
    
    
    #Read config.


    # projCP mode.
    #if args.command == 'projCP':
    #    wdforty.misc.projCP(config['projCP']['destination'])

    # storageHammer
    #if args.command == 'storageHammer':
    #    PIs = config['storageHammer']['PIs'].split(',')
    #    prefix = config['storageHammer']['prefix']
    #    postfix = config['storageHammer']['postfix']
    #    wdforty.misc.storageHammer(PIs, prefix, postfix)

    # catRun
    #if args.command == 'catRun':
    #    print("doing the CAT")
    #    #try:
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

    #if args.command == 'barDiag':
    #    print("diagnosing some barcodes.")
        #ssDic = wdforty.barDiag.parseSS('SampleSheet.csv')
        #print(ssDic)
        #UndComb = wdforty.barDiag.parseUnd()
        #print(UndComb)
        #revSS = wdforty.barDiag.revP5('SampleSheet.csv')
        #for i in revSS:
        #    print(','.join(i))

    #if args.command == 'bigClump':
        #print("Hammerclumps. Sit tight, this takes a while.")
        #wdforty.Clump.clumpRunner(config['QC']['clumpifyPath'], config['QC']['splitFQPath'])

    #if args.command == 'QC':
    #    print("Running fastqc&multiqc")
        #fastQC = config['QC']['fastQCPath']
        #multiQC = config['QC']['multiQCPath']
        #wdforty.QC.fastQCrunner(fastQC, multiQC)

    #if args.command == 'QCScreen':
    #    fastqScreen = config['QC']['fqScreenPath']
    #    seqtk = config['QC']['seqtkPath']
    #    screenconf = config['QC']['fqScreenConf']
    #    wdforty.QCScreen.screenRunner(fastqScreen,screenconf, seqtk)
    
    #if args.command == 'umiCount':
    #    if not args.umiFqFile:
    #        print("Specify --umiFqFile (R1 or R2)")
    #        sys.exit()
    #    elif not args.umi:
    #        print("Specify --umi SEQUENCE")
    #        sys.exit()
    #    else:
    #        resDic = wdforty.umiCount.umiCounter(args.umi, args.umiFqFile)
    #        print(resDic)

    #if args.command == 'linkscReads':
    #    print("Linking some fqs inside 'fqs' dir.")
        #if not args.projects:
        #    print("Specify a project directory.")
        #    sys.exit()
        #else:
        #    wdforty.misc.scLinker(args.projects)

if __name__ == "__main__":
    main()