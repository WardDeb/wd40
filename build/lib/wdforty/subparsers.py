import argparse

def diag_args(parser):

    parser.formatter_class = lambda prog: argparse.RawDescriptionHelpFormatter(prog, width=100)
    # set description
    parser.description = "[bold cyan]Diagnose a flowcell.[/bold cyan]\n\n"
    parser.description += "Usage:\n"
    parser.description += "  wd40 diag ./ \n"
    parser.description += "  wd40 diag ./ --depth 20000\n\n"
    parser.description += "Args:\n"
    parser.description += "  [bold cyan]flowcellPath[/bold cyan]\t\tpath to flowcell\n\n"
    parser.description += "optional Args:\n"
    parser.description += "  [bold cyan]--depth/-d[/bold cyan]\t[1000000]\tMinimum read depth to assume succesful demux\n"

    parser._action_groups.pop()

    # required
    reqArgs = parser.add_argument_group('Required args')
    reqArgs.add_argument(
        'flowcellPath',
    )
    

    # optional
    optArgs = parser.add_argument_group('Optional args')
    optArgs.add_argument(
        '--depth',
        '-d', 
        dest='depth',
        type=int,
        default=1000000,
    )
    return parser

def rel_args(parser):
    parser.formatter_class = lambda prog: argparse.RawDescriptionHelpFormatter(prog, width=100)
    # set description
    parser.description = "[bold cyan]Release a flowcell.[/bold cyan]\n\n"
    parser.description += "Usage:\n"
    parser.description += "  wd40 rel ./ \n"
    parser.description += "  wd40 rel /path/to/flowcell\n\n"
    parser.description += "Args:\n"
    parser.description += "  [bold cyan]flowcellPath[/bold cyan]\t\tpath to flowcell\n\n"

    parser._action_groups.pop() #purge help
    # required
    reqArgs = parser.add_argument_group("Required args")
    reqArgs.add_argument(
        'flowcellPath'
    )
    return parser

def dsk_args(parser):
    parser.formatter_class = lambda prog: argparse.RawDescriptionHelpFormatter(prog, width=100)
    # set description
    parser.description = "List diskspace for relevant drives\n\n"
    parser.description += "Usage:\n"
    parser.description += "\twd40 dsk a\n"
    parser.description += "\twd40 dsk p \n\n"
    parser.description += "Args:\n"
    parser.description += "  [bold cyan]disktype[/bold cyan]\tall (a), processing (p), sequencing_data (s)\n\n"
    parser._action_groups.pop()
    return parser

def sd_args(parser):
    parser.formatter_class = lambda prog: argparse.RawDescriptionHelpFormatter(prog, width=100)
    # set description.
    parser.description = "sequence data tools.\n\n"
    parser.description = "Usage:\n"
    parser.description += "\twd40 sd <tool> <opts>\n\n"
    parser.description += "Args:\n"
    parser.description += "  [bold cyan]tool[/bold cyan]\tscFqLink"
    return parser


def park_args(prs):
    return prs