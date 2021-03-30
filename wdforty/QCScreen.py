import csv
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os
import glob
from reportlab.platypus import BaseDocTemplate, Table, Preformatted, Paragraph, Spacer, Image, Frame, NextPageTemplate, PageTemplate, TableStyle, PageBreak, ListFlowable, ListItem
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import BaseDocTemplate
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors, utils

# Taken directly from bcl2fastq.

def plotFastqScreen(fname, outName) :
    species=[]
    ohol=[]
    mhol=[]
    ohml=[]
    mhml=[]
    for line in csv.reader(open(fname, "r"), dialect="excel-tab") :
        if(len(line) == 0) :
            break
        if(line[0].startswith("#")) :
            continue
        if(line[0].startswith("Library")) or (line[0].startswith("Genome")):
            continue
        species.append(line[0])
        ohol.append(float(line[5]))
        mhol.append(float(line[7]))
        ohml.append(float(line[9]))
        mhml.append(float(line[11]))

    ohol = np.array(ohol)
    mhol = np.array(mhol)
    ohml = np.array(ohml)
    mhml = np.array(mhml)

    ind = np.arange(len(species))
    p1 = plt.bar(ind, tuple(ohol), color="#0000FF")
    p2 = plt.bar(ind, tuple(mhol), color="#6699FF", bottom=tuple(ohol))
    p3 = plt.bar(ind, tuple(ohml), color="#FF0000", bottom=tuple(ohol+mhol))
    p4 = plt.bar(ind, tuple(mhml), color="#FF6699", bottom=tuple(ohol+mhol+ohml))

    plt.title("%s" % fname.replace("_R1_screen.txt","").split("/")[-1])
    plt.ylabel("%")
    plt.ylim((0,105))
    plt.xticks(ind, species, rotation="vertical")
    plt.yticks(np.arange(0,110,10))
    plt.legend((p4[0], p3[0], p2[0], p1[0]), ("repeat", "conserved", "multimap", "unique"))
    plt.tight_layout()
    plt.savefig(outName)
    plt.close()

def qcscreenToPdf():
    stylesheet=getSampleStyleSheet()
    pdf = BaseDocTemplate("SequencingReport.pdf", pagesize=landscape(A4))
    topHeight=120 #The image is 86 pixels tall
    #fTL = Frame(pdf.leftMargin, pdf.height, width=pdf.width/2, height=topHeight, id="col1") #Fixed height
    #fTR = Frame(pdf.leftMargin+pdf.width/2, pdf.height, width=pdf.width/2, height=topHeight, id="col2")
    fB = Frame(pdf.leftMargin, pdf.bottomMargin, pdf.width, pdf.height-topHeight, id="bottom")
    fM = Frame(pdf.leftMargin, pdf.bottomMargin, pdf.width, pdf.height, id="main")

    elements = []
    #fastq_screen images
    elements.append(NextPageTemplate("FirstPage"))
    elements.append(Paragraph("Contaminant screen", stylesheet['title']))
    elements.append(Paragraph("Below are images generated on the output of fastq_screen. In short, 1 million reads are randomly taken from each indicated sample. These reads are then aligned against a variety of organisms (mouse, human, etc.). The resulting alignments are then categorized as follows:", stylesheet['Normal']))
    elements.append(ListFlowable([
        Paragraph("unique: aligns only a single time within a single species.", stylesheet['Normal']),
        Paragraph("multimap: aligns multiple times, but only within a single species.", stylesheet['Normal']),
        Paragraph("conserved: aligns a single time to each of two or more species.", stylesheet['Normal']),
        Paragraph("repeat: aligns multiple times to each of two or more species.", stylesheet['Normal'])],
        bulletType='bullet',
        start='circle'))
    elements.append(Spacer(0,30))
    elements.append(Paragraph("Ideally, the 'unique' and 'multimap' values will only be appreciably present in the species from which your sample should have arisen.", stylesheet['Normal']))
    elements.append(Spacer(0,30))
    elements.append(Paragraph("Note that as the mouse and human reference genomes are the best quality, many low complexity reads will align to them.", stylesheet['Normal']))
    elements.append(Spacer(0,30))
    elements.append(NextPageTemplate("RemainingPages"))
    fqs = glob.glob("QCscreenOut/*.png")
    fqs.sort()
    for fq in fqs:
        print(fq)
        img = utils.ImageReader(fq)
        iw, ih = img.getSize()
        iw = 0.7*iw
        ih = 0.7*ih
        elements.append(Image(fq, width=iw, height=ih, hAlign="LEFT"))

    pdf.addPageTemplates([PageTemplate(id="FirstPage", frames=[fM]),
        PageTemplate(id="RemainingPages", frames=[fM])]),
    pdf.build(elements)