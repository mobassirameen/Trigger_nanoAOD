#!/usr/bin/env python3
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module

#importing tools from nanoAOD processing set up to store the ratio histograms in a root file
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.examples.ttHTriggers_2l_3ch_module import *


def calc(filename, channel):
    if filename=='JetMETG':
        files = [
            "/eos/cms/store/group/phys_higgs/moameen/tthmlep/JetMET/2022EE/JetMET_Run2022G.root"
        ]
        print("processing........ 'JetMET_Run2022G.root'")
    
        preselection=""
        # Create unique output file name based on channel
        if channel == 'ee':
            output_hist_file = f"histos_JetMET_Run2022G_ee.root"
        elif channel == 'em':
            output_hist_file = f"histos_JetMET_Run2022G_em.root"
        else:
            output_hist_file = f"histos_JetMET_Run2022G_mm.root"
        # Run the PostProcessor for the current file
        p = PostProcessor(
            ".", 
            #files, cut=preselection, branchsel=None, maxEntries=10000, # remove maxEnteries while running over full datsets/mc. Keep it while testing
            #files, cut=preselection, branchsel=None, maxEntries=1000000, # remove maxEnteries while running over full datsets/mc. Keep it while testing
            files, cut=preselection, branchsel=None,
            modules=[TrigAnalysis(filename, channel)], 
            noOut=True, histFileName=output_hist_file, histDirName="histograms"
        )
        p.run()
    elif filename=='TTto2L2Nu':
        files = [
            "/eos/cms/store/group/phys_higgs/moameen/tthmlep/NanoTrees_forCMGRDF_100524/2022EE/TTto2L2Nu.root"
        ]
        print("processing........ 'TTto2L2Nu.root'")
    
        preselection=""
        # Create unique output file name based on channel
        if channel == 'ee':
            output_hist_file = f"histos_TTto2L2Nu_ee.root"
        elif channel == 'em':
            output_hist_file = f"histos_TTto2L2Nu_em.root"
        else:
            output_hist_file = f"histos_TTto2L2Nu_mm.root"
        # Run the PostProcessor for the current file
        p = PostProcessor(
            ".", 
            #files, cut=preselection, branchsel=None, maxEntries=10000, # remove maxEnteries while running over full datsets/mc. Keep it while testing
            #files, cut=preselection, branchsel=None, maxEntries=1000000, # remove maxEnteries while running over full datsets/mc. Keep it while testing
            files, cut=preselection, branchsel=None,
            modules=[TrigAnalysis(filename, channel)], 
            noOut=True, histFileName=output_hist_file, histDirName="histograms"
        )
        p.run()
    
def main():
    #######################################################################
    print("\n")
    calc('JetMETG', 'ee')
    print("Writing output for 'ee' channel for the era=G of JetMET data")
    print("\n")
    calc('JetMETG', 'em')
    print("Writing output for 'em' channel for the era=G of JetMET data")
    print("\n")
    calc('JetMETG', 'mm')
    print("Writing output for 'mm' channel for the era=G of JetMET data")
    print("\n")
    #######################################################################
    
    ########################################################################################
    calc('TTto2L2Nu', 'ee')
    print("Writing output for 'ee' channel for the 2022EE compaign of TTto2L2Nu mc sample")
    print("\n")
    calc('TTto2L2Nu', 'em')
    print("Writing output for 'em' channel for the 2022EE compaign of TTto2L2Nu mc sample")
    print("\n")
    calc('TTto2L2Nu', 'mm')
    print("Writing output for 'mm' channel for the 2022EE compaign of TTto2L2Nu mc sample")
    print(10*"\t", "(:- This is end my friend -:)")
    ########################################################################################

    
if __name__ == "__main__":
    sys.exit(main())
