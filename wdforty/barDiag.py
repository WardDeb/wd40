from Bio.Seq import Seq
import json

def parseSS(ss):
    ssDic = {}
    with open(ss) as f:
        for line in f:
            if not line.strip().startswith('[Data]') and not line.strip().startswith('Lane'):
                quer = line.strip().split(',')
                lane = quer[0]
                sample = quer[2]
                if lane not in ssDic:
                    ssDic[lane] = {}
                if len(line.strip().split(',')) == 5:
                    proj = quer[4]
                    p7 = quer[3]
                    if proj not in ssDic[lane]:
                        ssDic[lane][proj] = {sample:[p7]}
                    else:
                        ssDic[lane][proj][sample] = [p7]
                elif len(line.strip().split(',')) == 6:
                    proj = quer[5]
                    p7 = quer[3]
                    p5 = quer[4]
                    if proj not in ssDic[lane]:
                        ssDic[lane][proj] = {sample:[p7,p5]}
                    else:
                        ssDic[lane][proj][sample] = [p7,p5]
    return ssDic

def parseUnd():
    UndComb = {}
    with open('Stats/Stats.json') as f:
        stats = json.load(f)
        for lane in stats['UnknownBarcodes']:
            for comb in lane['Barcodes']:
                if lane['Barcodes'][comb] > 500000:
                    UndComb[comb] = lane['Barcodes'][comb]
    return UndComb



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

