from Bio.Seq import Seq
from Bio.Alphabet import generic_dna
import json

def grabUndetermineds():
    combDict = {}

##TODO This goes over the entire smaplesheet , we can improve it by adding a specific project to through
## Also reversin i7, in case it ever needs to be rced.
#with open(args.i, "r") as f:
#    with open("SampleSheet_rc.csv", "w+") as out_f: #Add it to the arg
#        for index, line in enumerate(f):
#            if index <2:
#                out_f.write(line)
#            else:
#                line = line.split(",")
#                print(line)
#                if line[5].split("\n")[0] not in args.p:
#                    out_f.write("{},{},{},{},{},{}".format(line[0],line[1],line[2],line[3],line[4],line[5]))
#                else:
#                    print(line)
#                    out_f.write("{},{},{},{},".format(line[0],line[1],line[2],line[3]))
#                    i5 = Seq(line[4], generic_dna).reverse_complement()
#                    out_f.write("{},{}".format(str(i5),line[5]))

