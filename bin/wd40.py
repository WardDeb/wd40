#!/usr/bin/env python3
import argparse
import wdforty.misc
import textwrap

parser = argparse.ArgumentParser(description='Here to make your life easy! fac.py <command> [<args>]')
parser.add_argument('command', type=str, choices = ['storageHammer', 'projCP', 'fastQC'],
                    help='Give the command you would like to perform. ')
args = parser.parse_args()

config = Facilitator.misc.getConfig()
if args.Command == 'projCP':
    Facilitator.misc.projCP(config['projCP']['destination'])

if args.Command == 'storageHammer':
    PIs = config['storageHammer']['PIs'].split(',')
    prefix = config['storageHammer']['prefix']
    postfix = config['storageHammer']['postfix']
    Facilitator.misc.storageHammer(PIs, prefix, postfix)

