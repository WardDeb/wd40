import os
import subprocess
import glob
import rich

def catRun(Projects, flowcells, baseDir):
    for proj in Projects:
        os.mkdir(proj)
        Samples = [sample for sample in os.listdir(os.path.join(baseDir,flowcells[0],proj)) if 'Sample_' in sample]
        rich.print("Project {}: found {} Samples ({})".format(proj, len(Samples), ','.join(Samples)))
        for sample in Samples:
            catOutDir = os.path.join(proj, sample)
            os.mkdir(catOutDir)
            # Get all R1s
            R1s = []
            R2s = []
            for flow in flowcells:
                R1 = [R1fq for R1fq in os.listdir(os.path.join(baseDir, flow, proj, sample)) if 'R1.fastq.gz' in R1fq]
                R1s.append(os.path.join(baseDir,flow, proj, sample,R1[0]))
                R2 = [R2fq for R2fq in os.listdir(os.path.join(baseDir, flow, proj, sample)) if 'R2.fastq.gz' in R2fq]
                R2s.append(os.path.join(baseDir,flow, proj, sample,R2[0]))
            if len(R1s) != len(flowcells):
                print("Wow, seems like there are samples missing, I'm stopping.")
                break
            #Catting time.
            catName = R1s[0].split('/')[-1]
            catcmdR1 = ['cat'] + R1s
            print(' '.join(catcmdR1))
            with open(os.path.join(catOutDir, catName), "w") as out1:
                subprocess.run(catcmdR1, stdout=out1)
            catName = R2s[0].split('/')[-1]
            catcmdR2 = ['cat'] + R2s
            print(' '.join(catcmdR2))
            with open(os.path.join(catOutDir, catName), "w") as out2:
                subprocess.run(catcmdR2, stdout=out2)
    return "Done."