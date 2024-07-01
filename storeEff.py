#!/usr/bin/env python3
'''
DESCRIPTION:
    Script to calculate and store the trigger efficiencies for both data and MC separately.
'''
#================
# Import modules
#================
from argparse import ArgumentParser
import ROOT
import os

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

def createEfficiencyHistogram(efficiency, name, title):
    hist = ROOT.TH1F(name, title, efficiency.GetTotalHistogram().GetNbinsX(), 
                     efficiency.GetTotalHistogram().GetXaxis().GetXmin(), 
                     efficiency.GetTotalHistogram().GetXaxis().GetXmax())
    for bin in range(1, efficiency.GetTotalHistogram().GetNbinsX() + 1):
        if efficiency.GetTotalHistogram().GetBinContent(bin) > 0:
            hist.SetBinContent(bin, efficiency.GetEfficiency(bin))
            hist.SetBinError(bin, efficiency.GetEfficiencyErrorLow(bin))  # Use the lower error bound
    return hist

def storeEfficiency(data_file, mc_file, era, output_data_file, output_mc_file):
    f_data = ROOT.TFile(data_file, "READ")
    f_mc = ROOT.TFile(mc_file, "READ")
    fdir_data = f_data.GetDirectory("twoleptonTriggers")
    fdir_mc = f_mc.GetDirectory("twoleptonTriggers")
    statOption = ROOT.TEfficiency.kFCP

    variables = ["lep1_pt", "lep2_pt", "lep1_eta", "lep2_eta"]
    triggers = ["passedsignalANDreference"]

    output_f_data = ROOT.TFile(output_data_file, "RECREATE")
    output_f_mc = ROOT.TFile(output_mc_file, "RECREATE")

    for var in variables:
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

            # Create and fill histograms for efficiencies
            effs_data_hist = createEfficiencyHistogram(effs_data[trg], f'{var}_{trg}_data', f'{var} Efficiency (Data)')
            effs_mc_hist = createEfficiencyHistogram(effs_mc[trg], f'{var}_{trg}_mc', f'{var} Efficiency (MC)')
            output_f_data.cd()
            effs_data_hist.Write()
            output_f_mc.cd()
            effs_mc_hist.Write()

    output_f_data.Close()
    output_f_mc.Close()

def main(args):
    datasets = [
        {"data_file": "histos_2lssTrigger_DATA2022EE.root", 
         "mc_file": "histos_2lssTrigger_MC2022EE.root", 
         "era": "2022EE",
         "output_data_file": "efficiencies_2022EE_data.root",
         "output_mc_file": "efficiencies_2022EE_mc.root"
         },
        {"data_file": "histos_2lssTrigger_DATA2022.root", 
         "mc_file": "histos_2lssTrigger_MC2022.root", 
         "era": "2022",
         "output_data_file": "efficiencies_2022_data.root",
         "output_mc_file": "efficiencies_2022_mc.root"
         }
    ]
    
    for dataset in datasets:
        storeEfficiency(dataset["data_file"], dataset["mc_file"], dataset["era"], dataset["output_data_file"], dataset["output_mc_file"])

if __name__ == "__main__":
    VERBOSE = True

    parser = ArgumentParser(description="Derive the trigger scale factors for data and MC")
    parser.add_argument("-v", "--verbose", dest="verbose", default=VERBOSE, action="store_true", help="Verbose mode for debugging purposes [default: %s]" % (VERBOSE))

    args = parser.parse_args()
    main(args)
