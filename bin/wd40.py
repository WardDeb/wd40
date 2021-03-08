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
import os


def main():
    config = wdforty.misc.getConfig()
    arguments_info = {
        "noArgs": {
            "barDiag": ("Diagnose some common mistakes in sampleSheet file. "
                        "Parses stats (bcl2fastq) and sampleSheet.csv. "
                        "Run from a flowcell folder."),
            "bigClump": ("Run clumpify.sh serially, "
                         "in case your fastq files are huge."),
            "projCP": ("Copy over multiQC's and Contamination reports"),
            "storHam": ("Iterate over processing volumes "
                        "/ PI folders and list those that are nearly full. "
                        "(locations defined in wd40.ini)."),
            "FastQC": ("Run FastQC and multiQC from a flowcell folder. "
                       "Handy if you generated these with catRun."),
            "QCScreen": ("Run fastq_screen on a flowcell folder.")
        },
        "Args": {
            "catRun": ("Cat together fastq files from multiple flowcells."),
            "umiCount": ("Run umi demux. Specify project dir."),
            "linkSCReads": ("link fqs using cellranger nomenclature.")
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
                 'storHam',
                 'FastQC',
                 'QCScreen',
                 'umiCount',
                 'linkscReads'],
        help=argparse.SUPPRESS)
    parser.add_argument(
        '--flowCells',
        required=False,
        help=argparse.SUPPRESS
    )
    parser.add_argument(
        '--projects',
        required=False,
        help=argparse.SUPPRESS
    )
    parser.formatter_class = lambda prog: argparse.RawDescriptionHelpFormatter(
        prog,
        max_help_position=25,
        width=90)
    parser.description = textwrap.dedent('''
                wd40.py - Universal lubricant.

                Usage: wd40.py [command]

                ''')

    for argTyp in arguments_info:
        if argTyp == 'noArgs':
            parser.description += ("Commands without arguments "
                                   "(runs from workDir):\n")
        elif argTyp == 'Args':
            parser.description += "Commands requiring arguments:\n"
        for comm in arguments_info[argTyp]:
            parser.description += "    {}\t\t{}\n".format(
                comm,
                arguments_info[argTyp][comm])
    parser.description += "\n"

    if len(sys.argv[1:]) == 0:
        parser.print_help()
        sys.exit()

    args = parser.parse_args()

    # noArgs functions.
    # projCP mode.
    if args.command == 'projCP':
        rich.print("[bold cyan]ProjCP invoked![/bold cyan]")
        wdforty.misc.projCP(config['projCP']['destination'])

    # storHam
    if args.command == 'storHam':
        rich.print("[bold cyan]storHammering.[/bold cyan]")
        PIs = config['storageHammer']['PIs'].split(',')
        prefix = config['storageHammer']['prefix']
        postfix = config['storageHammer']['postfix']
        wdforty.misc.storageHammer(PIs, prefix, postfix)

    # bigClump
    if args.command == 'bigClump':
        rich.print("[bold cyan]Serial Clumpification invoked.[/bold cyan]")
        wdforty.Clump.clumpRunner(
            config['QC']['clumpifyPath'],
            config['QC']['splitFQPath'])

    # catRun
    if args.command == 'catRun':
        if not args.flowCells or not args.projects:
            rich.print(("Please specify [bold cyan]flowcells[/bold cyan] "
                        "using --flowCells Flowcell1,Flowcell2,Flowcell3"))
            rich.print(("Please specify [bold cyan]projects[/bold cyan] "
                        "using --projects Project1,Project2"))
            sys.exit()
        else:
            projects = args.projects.replace(' ', '').split(',')
            flowCells = args.flowCells.replace(' ', '').split(',')
            for proj in projects:
                if os.path.exists(proj):
                    rich.print(("[bold red]Directory {} already exists. "
                                "Please run this command in a location "
                                "that does not contain the projects "
                                "to be catted.[/bold red]".format(proj)))
                    sys.exit()
        baseDir = config['catRun']['baseDir']
        wdforty.catRun.catRun(projects, flowCells, baseDir)

    # FastQC
    if args.command == 'FastQC':
        rich.print("Running fastqc and multiqc")
        fastQC = config['QC']['fastQCPath']
        multiQC = config['QC']['multiQCPath']
        wdforty.QC.fastQCrunner(fastQC, multiQC)

    # if args.command == 'barDiag':
    #    print("diagnosing some barcodes.")
        # ssDic = wdforty.barDiag.parseSS('SampleSheet.csv')
        # print(ssDic)
        # UndComb = wdforty.barDiag.parseUnd()
        # print(UndComb)
        # revSS = wdforty.barDiag.revP5('SampleSheet.csv')
        # for i in revSS:
        #    print(','.join(i))

    # if args.command == 'QCScreen':
    #    fastqScreen = config['QC']['fqScreenPath']
    #    seqtk = config['QC']['seqtkPath']
    #    screenconf = config['QC']['fqScreenConf']
    #    wdforty.QCScreen.screenRunner(fastqScreen,screenconf, seqtk)

    # if args.command == 'umiCount':
    #    if not args.umiFqFile:
    #        print("Specify --umiFqFile (R1 or R2)")
    #        sys.exit()
    #    elif not args.umi:
    #        print("Specify --umi SEQUENCE")
    #        sys.exit()
    #    else:
    #        resDic = wdforty.umiCount.umiCounter(args.umi, args.umiFqFile)
    #        print(resDic)

    # if args.command == 'linkscReads':
    #    print("Linking some fqs inside 'fqs' dir.")
        # if not args.projects:
        #    print("Specify a project directory.")
        #    sys.exit()
        # else:
        #    wdforty.misc.scLinker(args.projects)


if __name__ == "__main__":
    main()
