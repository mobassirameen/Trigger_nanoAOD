#!/usr/bin/env python3
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module

#importing tools from nanoAOD processing set up to store the ratio histograms in a root file
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.examples.ttHTriggers_module import *

preselection=""
'''
files=["/eos/cms/store/group/phys_higgs/moameen/tthmlep/NanoTrees_forCMGRDF_100524/2022EE/Muon_Run2022E.root",
       "/eos/cms/store/group/phys_higgs/moameen/tthmlep/NanoTrees_forCMGRDF_100524/2022EE/Muon_Run2022F.root",
       "/eos/cms/store/group/phys_higgs/moameen/tthmlep/NanoTrees_forCMGRDF_100524/2022EE/Muon_Run2022G.root",
       ]
reference_paths = ["PFMET120_PFMHT120_IDTight"]
signal_paths = ["Ele32_WPTight_Gsf", "IsoMu24", "IsoMu27", "PFMETTypeOne140_PFMHT140_IDTight", "Ele23_Ele12_CaloIdL_TrackIdL_IsoVL", "Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8", "Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ"]
p=PostProcessor(".",files,cut=preselection,branchsel=None,modules=[TrigAnalysis(reference_paths,signal_paths)],noOut=True,histFileName="histos_2lssTrig_data2022postEE_v1.root",histDirName="metTrigAnalyzerNanoAOD")
p.run()
'''

Data2022preEE_files = [
    "/eos/cms/store/group/phys_higgs/moameen/tthmlep/NanoTrees_forCMGRDF_100524/2022/EGamma_Run2022C.root",
    "/eos/cms/store/group/phys_higgs/moameen/tthmlep/NanoTrees_forCMGRDF_100524/2022/MuonEG_Run2022C.root",
    "/eos/cms/store/group/phys_higgs/moameen/tthmlep/NanoTrees_forCMGRDF_100524/2022/Muon_Run2022C.root",
    "/eos/cms/store/group/phys_higgs/moameen/tthmlep/NanoTrees_forCMGRDF_100524/2022/EGamma_Run2022D.root",
    "/eos/cms/store/group/phys_higgs/moameen/tthmlep/NanoTrees_forCMGRDF_100524/2022/MuonEG_Run2022D.root",
    "/eos/cms/store/group/phys_higgs/moameen/tthmlep/NanoTrees_forCMGRDF_100524/2022/Muon_Run2022D.root",
]
Data2022postEE_files = [
    "/eos/cms/store/group/phys_higgs/moameen/tthmlep/NanoTrees_forCMGRDF_100524/2022EE/EGamma_Run2022E.root",
    "/eos/cms/store/group/phys_higgs/moameen/tthmlep/NanoTrees_forCMGRDF_100524/2022EE/MuonEG_Run2022E.root",
    "/eos/cms/store/group/phys_higgs/moameen/tthmlep/NanoTrees_forCMGRDF_100524/2022EE/Muon_Run2022E.root",
    "/eos/cms/store/group/phys_higgs/moameen/tthmlep/NanoTrees_forCMGRDF_100524/2022EE/EGamma_Run2022F.root",
    "/eos/cms/store/group/phys_higgs/moameen/tthmlep/NanoTrees_forCMGRDF_100524/2022EE/MuonEG_Run2022F.root",
    "/eos/cms/store/group/phys_higgs/moameen/tthmlep/NanoTrees_forCMGRDF_100524/2022EE/Muon_Run2022F.root",
    "/eos/cms/store/group/phys_higgs/moameen/tthmlep/NanoTrees_forCMGRDF_100524/2022EE/EGamma_Run2022G.root",
    "/eos/cms/store/group/phys_higgs/moameen/tthmlep/NanoTrees_forCMGRDF_100524/2022EE/MuonEG_Run2022G.root",
    "/eos/cms/store/group/phys_higgs/moameen/tthmlep/NanoTrees_forCMGRDF_100524/2022EE/Muon_Run2022G.root",
]
MC2022preEE_files = [
    "/eos/cms/store/group/phys_higgs/moameen/tthmlep/NanoTrees_forCMGRDF_100524/2022/WtoLNu_2Jets.root",
    "/eos/cms/store/group/phys_higgs/moameen/tthmlep/NanoTrees_forCMGRDF_100524/2022/TbarWplusto2L2Nu.root",
    "/eos/cms/store/group/phys_higgs/moameen/tthmlep/NanoTrees_forCMGRDF_100524/2022/TWminusto2L2Nu.root",
    "/eos/cms/store/group/phys_higgs/moameen/tthmlep/NanoTrees_forCMGRDF_100524/2022/WWto2L2Nu.root",
    "/eos/cms/store/group/phys_higgs/moameen/tthmlep/NanoTrees_forCMGRDF_100524/2022/WZto3LNu.root",
    "/eos/cms/store/group/phys_higgs/moameen/tthmlep/NanoTrees_forCMGRDF_100524/2022/ZZto4L.root",
]
MC2022postEE_files = [
    "/eos/cms/store/group/phys_higgs/moameen/tthmlep/NanoTrees_forCMGRDF_100524/2022EE/WtoLNu_2Jets.root",
    "/eos/cms/store/group/phys_higgs/moameen/tthmlep/NanoTrees_forCMGRDF_100524/2022EE/TbarWplusto2L2Nu.root",
    "/eos/cms/store/group/phys_higgs/moameen/tthmlep/NanoTrees_forCMGRDF_100524/2022EE/TWminusto2L2Nu.root",
    "/eos/cms/store/group/phys_higgs/moameen/tthmlep/NanoTrees_forCMGRDF_100524/2022EE/WWto2L2Nu.root",
    "/eos/cms/store/group/phys_higgs/moameen/tthmlep/NanoTrees_forCMGRDF_100524/2022EE/WZto3LNu.root",
    "/eos/cms/store/group/phys_higgs/moameen/tthmlep/NanoTrees_forCMGRDF_100524/2022EE/ZZto4L.root",
]


# Combine all file lists into a dictionary for easier processing
file_groups = {
    "DATA2022": Data2022preEE_files,
    "DATA2022EE": Data2022postEE_files,
    "MC2022": MC2022preEE_files,
    "MC2022EE": MC2022postEE_files,
}

reference_paths = ["PFMET120_PFMHT120_IDTight"]
signal_paths = ["Ele32_WPTight_Gsf", "IsoMu24", "IsoMu27", "PFMETTypeOne140_PFMHT140_IDTight", "Ele23_Ele12_CaloIdL_TrackIdL_IsoVL", "Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8", "Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ"]

# Running PostProcessor for each file group separately
for group_name, files in file_groups.items():
    print("Processing files are ======>", files)
    
    # Create unique output file name for the group
    output_hist_file = f"histos_TrigNanoAOD_{group_name}.root"
        
    # Run the PostProcessor for the current file
    p = PostProcessor(
        "/eos/cms/store/group/phys_higgs/moameen/tthmlep/Histos_TrigNanoAOD", 
        files, cut=preselection, branchsel=None, #maxEntries=1000000, # remove maxEnteries while running over full datsets/mc. Keep it while testing
        modules=[TrigAnalysis(reference_paths, signal_paths)], 
        noOut=True, histFileName=output_hist_file, histDirName="2lssTrigger"
    )
    p.run()
    print("\n")
    print(150*"#")
    print("Done for the files =======>", files)
    print(150*"#")
    print("\n")
