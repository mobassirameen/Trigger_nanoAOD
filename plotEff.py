#!/usr/bin/env python3
'''
DESCRIPTION:


'''
#================
# Import modules
#================
from argparse import ArgumentParser
import ROOT
import math 
import time

def getCanvas():
    d = ROOT.TCanvas("", "", 800, 700)
    d.SetLeftMargin(0.12)
    d.SetRightMargin(0.15)
    d.SetLeftMargin(0.13)
    return d

def AddPrivateWorkText(setx=0.21, sety=0.905):
    tex = ROOT.TLatex(0.,0., 'Private Work');
    tex.SetNDC();
    tex.SetX(setx);
    tex.SetY(sety);
    tex.SetTextFont(53);
    tex.SetTextSize(28);
    tex.SetLineWidth(2)
    return tex

def AddCMSText(setx=0.205, sety=0.905):
    texcms = ROOT.TLatex(0.,0., 'CMS');
    texcms.SetNDC();
    texcms.SetTextAlign(31);
    texcms.SetX(setx);
    texcms.SetY(sety);
    texcms.SetTextFont(63);
    texcms.SetLineWidth(2);
    texcms.SetTextSize(30);
    return texcms

def createLegend():
    legend = ROOT.TLegend(0.30, 0.30, 0.82, 0.50)
    legend.SetFillColor(0)
    legend.SetFillStyle(0);
    legend.SetBorderSize(0);
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
          

def main(args):

    f = ROOT.TFile(args.rfile, "READ")
    #fdir = f.GetDirectory("metTrigAnalyzerNanoAOD")
    fdir = f.GetDirectory("twoleptonTriggers")
    statOption = ROOT.TEfficiency.kFCP

    #variables  = ["met_pt", "pv"]
    variables  = ["lep1_pt", "lep1_eta"]
    #triggers   = ["passed", "passtrig_HLT_Ele32_WPTight_Gsf", "passtrig_HLT_IsoMu24", "passtrig_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL"]
    #triggers   = ["passed", "passtrig_HLT_Ele32_WPTight_Gsf"]
    triggers   = ["passedsignalANDreference"]

    for var in variables:
        c = getCanvas()
        leg = createLegend()
        #den = fdir.Get(f'h_{var}_all')
        den = fdir.Get(f'h_{var}_passedreftrig')

        nums = {}
        effs = {}
        for j, trg in enumerate(triggers):
            nums[trg] = fdir.Get(f'h_{var}_{trg}')
            effs[trg] = ROOT.TEfficiency(nums[trg], den)
            effs[trg].SetStatisticOption(statOption)
            effs[trg] = SetStyle(effs[trg], colors[j])
            if j == 0:
                effs[trg].Draw()
            else:
                effs[trg].Draw("same")
            leg.AddEntry(effs[trg], trg.replace("passtrig_HLT", "HLT").replace("passedsignalANDreference", "logical OR"), "ep")
                
        c.Modified()
        c.Update()
        effs["passedsignalANDreference"].GetPaintedGraph().GetYaxis().SetRangeUser(0.0, 1.2)
        effs["passedsignalANDreference"].GetPaintedGraph().GetYaxis().SetTitle("#varepsilon_{L1+HLT}")
        leg.Draw("same")
        
        # Styling stuff
        tex_cms = AddCMSText()
        tex_cms.Draw("same")
        
        private = AddPrivateWorkText()
        private.Draw("same")
        
        header = ROOT.TLatex()
        header.SetTextSize(0.04)
        header.DrawLatexNDC(0.57, 0.905, "2022EE, #sqrt{s} = 13.6 TeV")
        
        c.Update()
        c.Modified()
        for fs in args.formats:
            savename = f'plots/TrgEffs_{var}{fs}'
            c.SaveAs(savename)
            

    # Plot 2D:
    c2D = getCanvas()

    den = fdir.Get('h_lep1_eta_vs_pt_passedreftrig')
    num = fdir.Get('h_lep1_eta_vs_pt_passedsignalANDreference')
    
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
    header.DrawLatexNDC(0.57, 0.905, "2022EE, #sqrt{s} = 13.6 TeV")
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
    for fs in args.formats:
        c2D.SaveAs("plots/Eff2D_trigger_EtavsPt%s" % (fs))     
    
    # Print the numerical efficiency values
    #print("Efficiency values (eta, pt, efficiency):")
    #for x_bin in range(1, eff2D.GetTotalHistogram().GetNbinsX() + 1):
        #for y_bin in range(1, eff2D.GetTotalHistogram().GetNbinsY() + 1):
            #if eff2D.GetTotalHistogram().GetBinContent(x_bin, y_bin) != 0:  # Check to avoid division by zero
                #eta = eff2D.GetTotalHistogram().GetXaxis().GetBinCenter(x_bin)
                #pt = eff2D.GetTotalHistogram().GetYaxis().GetBinCenter(y_bin)
                #efficiency = eff2D.GetEfficiency(eff2D.GetGlobalBin(x_bin, y_bin))
                #print(f"eta: {eta}, pt: {pt}, efficiency: {efficiency}")

if __name__ == "__main__":

    VERBOSE       = True
    YEAR          = "2022EE"
    #TRGROOTFILE   = "histos_2lssTrigger_DATA2022EE.root"
    #TRGROOTFILE   = "histos_2lssTrigger_pt_eta_DATA2022EE.root"
    TRGROOTFILE   = "histos_2lssTrigger_pt_eta_1D_2D_DATA2022EE.root"
    FORMATS       = ['.png', '.pdf']

    parser = ArgumentParser(description="Derive the trigger scale factors")
    parser.add_argument("-v", "--verbose", dest="verbose", default=VERBOSE, action="store_true", help="Verbose mode for debugging purposes [default: %s]" % (VERBOSE))
    parser.add_argument("--rfile", dest="rfile", type=str, action="store", default=TRGROOTFILE, help="ROOT file containing the denominators and numerators [default: %s]" % (TRGROOTFILE))
    parser.add_argument("--year", dest="year", action="store", default=YEAR, help="Process year")
    parser.add_argument("--formats", dest="formats", default=FORMATS, action="store", help="Formats to save histograms")

    args = parser.parse_args()
    main(args)
