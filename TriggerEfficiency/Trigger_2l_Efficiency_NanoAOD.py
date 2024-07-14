#!/usr/bin/env python3
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module

#importing tools from nanoAOD processing set up to store the ratio histograms in a root file
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.examples.ttHTriggers_moduleTEST import *


def calc(filename):
    if filename=='JetMETG':
        files = [
            "/eos/cms/store/group/phys_higgs/moameen/tthmlep/JetMET/2022EE/JetMET_Run2022G.root"
        ]
        print("processing........ 'JetMET_Run2022G.root'")
    
        preselection=""
        # Create unique output file name for the group
        output_hist_file = f"histos_JetMET_Run2022G_testJul2024.root"
        # Run the PostProcessor for the current file
        p = PostProcessor(
            ".", 
            #files, cut=preselection, branchsel=None, maxEntries=10000, # remove maxEnteries while running over full datsets/mc. Keep it while testing
            #files, cut=preselection, branchsel=None, maxEntries=1000000, # remove maxEnteries while running over full datsets/mc. Keep it while testing
            files, cut=preselection, branchsel=None,
            modules=[TrigAnalysis(filename)], 
            noOut=True, histFileName=output_hist_file, histDirName="histograms"
        )
        p.run()
    elif filename=='TTto2L2Nu':
        files = [
            "/eos/cms/store/group/phys_higgs/moameen/tthmlep/NanoTrees_forCMGRDF_100524/2022EE/TTto2L2Nu.root"
        ]
        print("processing........ 'TTto2L2Nu.root'")
    
        preselection=""
        # Create unique output file name for the group
        output_hist_file = f"histos_TTto2L2Nu_testJul2024.root"
        # Run the PostProcessor for the current file
        p = PostProcessor(
            ".", 
            files, cut=preselection, branchsel=None, maxEntries=100000, # remove maxEnteries while running over full datsets/mc. Keep it while testing
            #files, cut=preselection, branchsel=None, maxEntries=1000000, # remove maxEnteries while running over full datsets/mc. Keep it while testing
            #files, cut=preselection, branchsel=None,
            modules=[TrigAnalysis(filename)], 
            noOut=True, histFileName=output_hist_file, histDirName="histograms"
        )
        p.run()
    
def main():
    calc('JetMETG')
    calc('TTto2L2Nu')
    
if __name__ == "__main__":
    sys.exit(main())
