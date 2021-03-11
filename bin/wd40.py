#!/usr/bin/env python3
import argparse
import textwrap
import wdforty.misc
import wdforty.catRun
import wdforty.barDiag
import wdforty.QC
import wdforty.Clump
import rich
import sys
import os
import pandas as pd


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
    parser.add_argument(
        '--depth',
        required=False,
        help=argparse.SUPPRESS,
        type=int,
        default=1000000
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
            rich.print("[bold cyan]catRun invoked![/bold cyan]")
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
        rich.print("[bold cyan]QC invoked![/bold cyan]")
        fastQC = config['QC']['fastQCPath']
        multiQC = config['QC']['multiQCPath']
        wdforty.QC.fastQCrunner(fastQC, multiQC)

    # barDiag
    if args.command == 'barDiag':
        rich.print(
            "[bold cyan]barDiag invoked![/bold cyan]"
            )
        rich.print(
            "Looking for [bold cyan]{}[/bold cyan] reads".format(args.depth)
            )
        rich.print("Use [bold cyan]--depth INT[/bold cyan] to change.")
        if not os.path.exists('SampleSheet.csv'):
            rich.print('There is no SampleSheet.csv file.')
            sys.exit()
        else:
            ssdf, pairedStatus = wdforty.barDiag.parseSS("SampleSheet.csv")
        if not os.path.exists('Stats/Stats.json'):
            rich.print('There is no Stats/Stats.json file.')
            sys.exit()
        else:
            candidates = wdforty.barDiag.parseUnd(
                "Stats/Stats.json", args.depth
                )
        rich.print("[bold red]Undetermined candidates:[/bold red]")
        rich.print(candidates)
        rich.print("[bold red]Badly demux'ed samples:[/bold red]")
        rich.print(ssdf[ssdf['readCount'] < args.depth]['Sample_Name'])
        updateDF, nChanges = wdforty.barDiag.crapMatcher(ssdf, pairedStatus, candidates, args.depth)
        rich.print("A total of {} combinations have been changed.".format(nChanges))
        if nChanges > 0:
            if os.path.exists('SampleSheet_new.csv'):
                os.remove('SampleSheet_new.csv')
            with open('SampleSheet_new.csv', 'w') as f:
                f.write('[Data]')
            updateDF.to_csv('SampleSheet_new.csv', index=False)
            rich.print("New sampleSheet written.")


if __name__ == "__main__":
    main()
