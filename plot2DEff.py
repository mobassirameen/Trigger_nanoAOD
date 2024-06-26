#!/usr/bin/env python3
'''
DESCRIPTION:


'''
#================
# Import modules
#================
from argparse import ArgumentParser
import ROOT
import os

def getCanvas():
    d = ROOT.TCanvas("", "", 800, 700)
    d.SetLeftMargin(0.12)
    d.SetRightMargin(0.15)
    d.SetLeftMargin(0.13)
    return d

def AddPrivateWorkText(setx=0.21, sety=0.905):
    tex = ROOT.TLatex(0.,0., 'Private Work')
    tex.SetNDC()
    tex.SetX(setx)
    tex.SetY(sety)
    tex.SetTextFont(53)
    tex.SetTextSize(28)
    tex.SetLineWidth(2)
    return tex

def AddCMSText(setx=0.205, sety=0.905):
    texcms = ROOT.TLatex(0.,0., 'CMS')
    texcms.SetNDC()
    texcms.SetTextAlign(31)
    texcms.SetX(setx)
    texcms.SetY(sety)
    texcms.SetTextFont(63)
    texcms.SetLineWidth(2)
    texcms.SetTextSize(30)
    return texcms

def createLegend():
    legend = ROOT.TLegend(0.30, 0.30, 0.82, 0.50)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)
    legend.SetTextSize(0.03)  # Set text size
    return legend

def SetStyle(h, color, marker_style):
    h.SetLineColor(color)
    h.SetMarkerColor(color)
    h.SetMarkerStyle(marker_style)
    return h

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetTextFont(42)

def SetStyle(h, COLOR):
    h.SetMarkerStyle(20)
    h.SetMarkerColor(COLOR)
    h.SetLineColor(COLOR)
    return h

colors = {0: ROOT.kBlack,
          1: ROOT.kBlue,
          2: ROOT.kGreen+1,
          3: ROOT.kRed+1,
          4: ROOT.kOrange-3,
          5: ROOT.kMagenta+2,
          6: ROOT.kTeal+3,
          }

def draw2DEfficiency(fdir, lep, era, datatype, args):
    # Plot 2D:
    c2D = getCanvas()

    den = fdir.Get(f'h_{lep}_eta_vs_pt_passedreftrig')
    num = fdir.Get(f'h_{lep}_eta_vs_pt_passedsignalANDreference')
    
    eff2D = ROOT.TEfficiency(num, den)
    eff2D.Draw("COLZ")
    c2D.Modified()
    c2D.Update()
    
    tex_cms = AddCMSText()
    tex_cms.Draw("same")
    private = AddPrivateWorkText()
    private.Draw("same")
    header = ROOT.TLatex()
    header.SetTextSize(0.04)
    header.DrawLatexNDC(0.57, 0.905, f"{datatype}, {era}, #sqrt{{s}} = 13.6 TeV")
    c2D.Update()
    c2D.Modified()
    
    # Print the efficiency values on the plot
    latex = ROOT.TLatex()
    latex.SetTextSize(0.02)
    latex.SetTextAlign(22)  # Center alignment
    for x_bin in range(1, eff2D.GetTotalHistogram().GetNbinsX() + 1):
        for y_bin in range(1, eff2D.GetTotalHistogram().GetNbinsY() + 1):
            if eff2D.GetTotalHistogram().GetBinContent(x_bin, y_bin) != 0:  # Check to avoid division by zero
                eta = eff2D.GetTotalHistogram().GetXaxis().GetBinCenter(x_bin)
                pt = eff2D.GetTotalHistogram().GetYaxis().GetBinCenter(y_bin)
                efficiency = eff2D.GetEfficiency(eff2D.GetGlobalBin(x_bin, y_bin))
                efficiency_text = f"{efficiency:.2f}"
                latex.DrawLatex(eta, pt, efficiency_text)

    c2D.Update()
    c2D.Modified()
    
    # Save the plot in specified formats
    outdir = f"/eos/user/m/moameen/www/TriggerStudyPlots/{era}"
    os.makedirs(outdir, exist_ok=True)
    for fs in args.formats:
        c2D.SaveAs(os.path.join(outdir, f"Eff2D_trigger_{lep}_eta_vs_pt_{datatype}_{era}{fs}"))
    
def main(args):

    files = {
        "DATA2022": ("histos_2lssTrigger_DATA2022.root", "Data", "2022"),
        "DATA2022EE": ("histos_2lssTrigger_DATA2022EE.root", "Data", "2022EE"),
        "MC2022": ("histos_2lssTrigger_MC2022.root", "MC", "2022"),
        "MC2022EE": ("histos_2lssTrigger_MC2022EE.root", "MC", "2022EE")
    }

    for key, (filename, datatype, era) in files.items():
        f = ROOT.TFile(os.path.join(args.indir, filename), "READ")
        fdir = f.GetDirectory("twoleptonTriggers")
        statOption = ROOT.TEfficiency.kFCP

        for leps in ['lep1', 'lep2']:
            draw2DEfficiency(fdir, leps, era, datatype, args)

if __name__ == "__main__":

    VERBOSE       = True
    FORMATS       = ['.png']

    parser = ArgumentParser(description="Derive the trigger scale factors")
    parser.add_argument("-v", "--verbose", dest="verbose", default=VERBOSE, action="store_true", help="Verbose mode for debugging purposes [default: %s]" % (VERBOSE))
    parser.add_argument("--indir", dest="indir", type=str, action="store", default="/eos/user/m/moameen/Trigger_nanoAOD", help="Directory containing ROOT files")
    parser.add_argument("--formats", dest="formats", default=FORMATS, action="store", help="Formats to save histograms")

    args = parser.parse_args()
    main(args)
