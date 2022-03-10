import argparse
import wdforty.misc
# import textwrap
# import wdforty.misc
# import wdforty.catRun
# import wdforty.barDiag
# import wdforty.QC
# import wdforty.Clump
# import wdforty.QCScreen
# import glob
# import rich
# import sys
# import os
# import pandas as pd


def main():
    parser = argparse.ArgumentParser(prog='wd40')
    parser.add_argument(
        '-c', '--config',
        default=None,
        help='specify an ini file to use as config.'
    )
    parser.add_argument(
        'release',
        help='Release a seq project. Fetches projects from cwd. Takes no arguments.'
    )

    subparsers = parser.add_subparsers(help='sub-command help')
    # sd - sequencing data
    parser_sd = subparsers.add_parser('sd', help='sequencing data functions.')
    parser_sd.add_argument(
        'mode',
        choices = ['']
    )
    parser_fc = subparsers.add_parser('fc', help='file/disk checks')
    args = parser.parse_args()
    # get config
    #config = wdforty.misc.getConfig()
    # arguments_info = {
    #     "noArgs": {
    #         "barDiag": ("Diagnose some common mistakes in sampleSheet file. "
    #                     "Parses stats (bcl2fastq) and sampleSheet.csv. "
    #                     "Run from a flowcell folder."),
    #         "bigClump": ("Run clumpify.sh serially, "
    #                      "in case your fastq files are huge."),
    #         "projCP": ("Copy over multiQC's and Contamination reports"),
    #         "storHam": ("Iterate over processing volumes "
    #                     "/ PI folders and list those that are nearly full. "
    #                     "(locations defined in wd40.ini)."),
    #         "FastQC": ("Run FastQC and multiQC from a flowcell folder. "
    #                    "Handy if you generated these with catRun."),
    #         "QCScreenPLOT": ("Searches for QCscreen txts and plots them."),
    #         "chModder": ("Open up permissions for projects in their end loc"),
    #         "sambaDup": ("Parse a bunch of markdup.txt files")
    #     },
    #     "Args": {
    #         "catRun": ("Cat together fastq files from multiple flowcells."),
    #         "umiCount": ("Run umi demux. Specify project dir."),
    #         "linkSCReads": ("link fqs using cellranger nomenclature.")
    #     }
    # }
    # parser = argparse.ArgumentParser("wd40.py", usage=argparse.SUPPRESS)
    # parser.add_argument(
    #     'command',
    #     type=str,
    #     choices=['barDiag',
    #              'bigClump',
    #              'catRun',
    #              'chModder',
    #              'projCP',
    #              'storHam',
    #              'FastQC',
    #              'QCScreenPLOT',
    #              'umiCount',
    #              'linkscReads',
    #              'sambaDup'],
    #     help=argparse.SUPPRESS)
    # parser.add_argument(
    #     '--flowCells',
    #     required=False,
    #     help=argparse.SUPPRESS
    # )
    # parser.add_argument(
    #     '--projects',
    #     required=False,
    #     help=argparse.SUPPRESS
    # )
    # parser.add_argument(
    #     '--depth',
    #     required=False,
    #     help=argparse.SUPPRESS,
    #     type=int,
    #     default=1000000
    # )
    # parser.add_argument(
    #     '--machine',
    #     required=False,
    #     help=argparse.SUPPRESS,
    #     type=str,
    #     default='novaSeq',
    #     choices=['novaSeq', 'nextSeq']
    # )
    # parser.formatter_class = lambda prog: argparse.RawDescriptionHelpFormatter(
    #     prog,
    #     max_help_position=25,
    #     width=90)
    # parser.description = textwrap.dedent('''
    #             wd40.py - Universal lubricant.

    #             Usage: wd40.py [command]

    #             ''')

    # for argTyp in arguments_info:
    #     if argTyp == 'noArgs':
    #         parser.description += ("Commands without arguments "
    #                                "(runs from workDir):\n")
    #     elif argTyp == 'Args':
    #         parser.description += "Commands requiring arguments:\n"
    #     for comm in arguments_info[argTyp]:
    #         parser.description += "    {}\t\t{}\n".format(
    #             comm,
    #             arguments_info[argTyp][comm])
    # parser.description += "\n"

    # if len(sys.argv[1:]) == 0:
    #     parser.print_help()
    #     sys.exit()

    # args = parser.parse_args()

    # # noArgs functions.
    # # sambaDup
    # if args.command == 'sambaDup':
    #     wdforty.misc.sambaDup()
    # # chModder
    # if args.command == 'chModder':
    #     wdforty.misc.chModder(config['storageHammer']['prefix'])
    # # projCP mode.
    # if args.command == 'projCP':
    #     rich.print("[bold cyan]ProjCP invoked![/bold cyan]")
    #     wdforty.misc.projCP(config['projCP']['destination'])

    # # storHam
    # if args.command == 'storHam':
    #     rich.print("[bold cyan]storHammering.[/bold cyan]")
    #     PIs = config['storageHammer']['PIs'].split(',')
    #     prefix = config['storageHammer']['prefix']
    #     postfix = config['storageHammer']['postfix']
    #     wdforty.misc.storageHammer(PIs, prefix, postfix)

    # # bigClump
    # if args.command == 'bigClump':
    #     rich.print("[bold cyan]Serial Clumpification invoked.[/bold cyan]")
    #     if args.machine:
    #         rich.print("[bold red]Setting clump opts for {}[/bold red]".format(args.machine))
    #         wdforty.Clump.clumpRunner(
    #             config['QC']['clumpifyPath'],
    #             config['QC']['splitFQPath'],
    #             args.machine)
    #     else:
    #         rich.print("[bold red]Setting clump opts for novaSeq[/bold red]")
    #         wdforty.Clump.clumpRunner(
    #             config['QC']['clumpifyPath'],
    #             config['QC']['splitFQPath'])


    # # catRun
    # if args.command == 'catRun':
    #     if not args.flowCells or not args.projects:
    #         rich.print(("Please specify [bold cyan]flowcells[/bold cyan] "
    #                     "using --flowCells Flowcell1,Flowcell2,Flowcell3"))
    #         rich.print(("Please specify [bold cyan]projects[/bold cyan] "
    #                     "using --projects Project1,Project2"))
    #         sys.exit()
    #     else:
    #         rich.print("[bold cyan]catRun invoked![/bold cyan]")
    #         projects = args.projects.replace(' ', '').split(',')
    #         flowCells = args.flowCells.replace(' ', '').split(',')
    #         for proj in projects:
    #             if os.path.exists(proj):
    #                 rich.print(("[bold red]Directory {} already exists. "
    #                             "Please run this command in a location "
    #                             "that does not contain the projects "
    #                             "to be catted.[/bold red]".format(proj)))
    #                 sys.exit()
    #     baseDir = config['catRun']['baseDir']
    #     wdforty.catRun.catRun(projects, flowCells, baseDir)

    # # FastQC
    # if args.command == 'FastQC':
    #     rich.print("[bold cyan]QC invoked![/bold cyan]")
    #     fastQC = config['QC']['fastQCPath']
    #     multiQC = config['QC']['multiQCPath']
    #     wdforty.QC.fastQCrunner(fastQC, multiQC)

    # # barDiag
    # if args.command == 'barDiag':
    #     rich.print(
    #         "[bold cyan]barDiag invoked![/bold cyan]"
    #         )
    #     rich.print(
    #         "Looking for [bold cyan]{}[/bold cyan] reads".format(args.depth)
    #         )
    #     rich.print("Use [bold cyan]--depth INT[/bold cyan] to change.")
    #     if not os.path.exists('SampleSheet.csv'):
    #         rich.print('There is no SampleSheet.csv file.')
    #         sys.exit()
    #     else:
    #         ssdf, pairedStatus = wdforty.barDiag.parseSS("SampleSheet.csv")
    #     if not os.path.exists('Stats/Stats.json'):
    #         rich.print('There is no Stats/Stats.json file.')
    #         sys.exit()
    #     else:
    #         candidates = wdforty.barDiag.parseUnd(
    #             "Stats/Stats.json", args.depth
    #             )
    #     rich.print("[bold red]Undetermined candidates:[/bold red]")
    #     rich.print(candidates)
    #     rich.print("[bold red]Badly demux'ed samples:[/bold red]")
    #     rich.print(ssdf[ssdf['readCount'] < args.depth]['Sample_Name'])
    #     if pairedStatus == True:
    #         updateDF, nChanges = wdforty.barDiag.crapMatcher(ssdf, pairedStatus, candidates, args.depth)
    #         rich.print("A total of {} combinations have been changed.".format(nChanges))
    #         if nChanges > 0:
    #             if os.path.exists('SampleSheet_new.csv'):
    #                 os.remove('SampleSheet_new.csv')
    #             with open('SampleSheet_new.csv', 'w') as f:
    #                 f.write('[Data]')
    #             updateDF.to_csv('SampleSheet_new.csv', index=False)
    #             rich.print("New sampleSheet written.")
    # if args.command == 'QCScreenPLOT':
    #     print("invoke QCscreenPLOT")
    #     if not os.path.exists("QCscreenOut"):
    #         os.mkdir("QCscreenOut")
    #         for screen in glob.glob("*/*_screen.txt"):
    #             print("Plotting {}".format(screen))
    #             outFile = os.path.join("QCscreenOut", screen.split('/')[-1].replace('_screen.txt', '.png'))
    #             wdforty.QCScreen.plotFastqScreen(screen, outFile)
    #     wdforty.QCScreen.qcscreenToPdf()

if __name__ == "__main__":
    main()