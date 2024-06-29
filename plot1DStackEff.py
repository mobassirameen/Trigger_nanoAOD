#!/usr/bin/env python3
'''
DESCRIPTION:
    Script to calculate and plot the trigger efficiencies for both data and MC stacks.
'''
#================
# Import modules
#================
from argparse import ArgumentParser
import ROOT
import math 
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

colors = {
    0: ROOT.kBlack,
    1: ROOT.kBlue,
    2: ROOT.kGreen+1,
    3: ROOT.kRed+1,
    4: ROOT.kOrange-3,
    5: ROOT.kMagenta+2,
    6: ROOT.kTeal+3,
}

def draw1DStackEfficiency(data_file, mc_file, era, formats):
    f_data = ROOT.TFile(data_file, "READ")
    f_mc = ROOT.TFile(mc_file, "READ")
    fdir_data = f_data.GetDirectory("twoleptonTriggers")
    fdir_mc = f_mc.GetDirectory("twoleptonTriggers")
    statOption = ROOT.TEfficiency.kFCP

    variables = ["lep1_pt", "lep2_pt", "lep1_eta", "lep2_eta"]
    triggers = ["passedsignalANDreference"]

    for var in variables:
        c = getCanvas()
        leg = createLegend()

        den_data = fdir_data.Get(f'h_{var}_passedreftrig')
        den_mc = fdir_mc.Get(f'h_{var}_passedreftrig')

        nums_data = {}
        effs_data = {}
        nums_mc = {}
        effs_mc = {}

        for j, trg in enumerate(triggers):
            nums_data[trg] = fdir_data.Get(f'h_{var}_{trg}')
            effs_data[trg] = ROOT.TEfficiency(nums_data[trg], den_data)
            effs_data[trg].SetStatisticOption(statOption)
            effs_data[trg] = SetStyle(effs_data[trg], colors[j], 20)

            nums_mc[trg] = fdir_mc.Get(f'h_{var}_{trg}')
            effs_mc[trg] = ROOT.TEfficiency(nums_mc[trg], den_mc)
            effs_mc[trg].SetStatisticOption(statOption)
            effs_mc[trg] = SetStyle(effs_mc[trg], colors[j+1], 21)

            if j == 0:
                effs_data[trg].Draw()
                effs_mc[trg].Draw("same")
            else:
                effs_data[trg].Draw("same")
                effs_mc[trg].Draw("same")
            
            leg.AddEntry(effs_data[trg], f"Data {trg.replace('passedsignalANDreference', '')}", "ep")
            leg.AddEntry(effs_mc[trg], f"MC {trg.replace('passedsignalANDreference', '')}", "ep")

        c.Modified()
        c.Update()
        effs_data["passedsignalANDreference"].GetPaintedGraph().GetYaxis().SetRangeUser(0.0, 1.2)
        effs_data["passedsignalANDreference"].GetPaintedGraph().GetYaxis().SetTitle("#varepsilon_{L1+HLT}")
        leg.Draw("same")

        # Styling
        tex_cms = AddCMSText()
        tex_cms.Draw("same")

        private = AddPrivateWorkText()
        private.Draw("same")

        header = ROOT.TLatex()
        header.SetTextSize(0.04)
        header.DrawLatexNDC(0.53, 0.905, f"{era}, #sqrt{{s}} = 13.6 TeV")

        c.Update()
        c.Modified()
        outdir = f"/eos/user/m/moameen/www/TriggerStudyPlots/{era}"
        os.makedirs(outdir, exist_ok=True)
        for fs in formats:
            savename = f'{outdir}/TriggerEff1D_{var}{fs}'
            c.SaveAs(savename)

def main(args):
    datasets = [
        {"data_file": "histos_2lssTrigger_DATA2022EE.root", 
         "mc_file": "histos_2lssTrigger_MC2022EE.root", 
         "era": "2022EE",
         },
        {"data_file": "histos_2lssTrigger_DATA2022.root", 
         "mc_file": "histos_2lssTrigger_MC2022.root", 
         "era": "2022",
         }
    ]
    
    for dataset in datasets:
        draw1DStackEfficiency(dataset["data_file"], dataset["mc_file"], dataset["era"], args.formats)

if __name__ == "__main__":
    VERBOSE = True
    FORMATS = ['.png', '.pdf']

    parser = ArgumentParser(description="Derive the trigger scale factors for data and MC")
    parser.add_argument("-v", "--verbose", dest="verbose", default=VERBOSE, action="store_true", help="Verbose mode for debugging purposes [default: %s]" % (VERBOSE))
    parser.add_argument("--formats", dest="formats", default=FORMATS, action="store", help="Formats to save histograms")

    args = parser.parse_args()
    main(args)

