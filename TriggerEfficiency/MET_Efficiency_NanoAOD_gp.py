#!/usr/bin/env python3
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module

#importing tools from nanoAOD processing set up to store the ratio histograms in a root file
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.examples.TrigMETAnalysis_module import *

preselection=""
files=["/eos/cms/store/group/phys_higgs/moameen/tthmlep/NanoTrees_forCMGRDF_100524/2022EE/Muon_Run2022E.root",
       "/eos/cms/store/group/phys_higgs/moameen/tthmlep/NanoTrees_forCMGRDF_100524/2022EE/Muon_Run2022F.root",
       "/eos/cms/store/group/phys_higgs/moameen/tthmlep/NanoTrees_forCMGRDF_100524/2022EE/Muon_Run2022G.root",
       ]
reference_paths = ["Ele32_WPTight_Gsf"]
signal_paths    = ["PFMET120_PFMHT120_IDTight", "PFMET130_PFMHT130_IDTight", "PFMET140_PFMHT140_IDTight", "PFMETTypeOne140_PFMHT140_IDTight", "PFMETNoMu120_PFMHTNoMu120_IDTight",
                   "PFMETNoMu130_PFMHTNoMu130_IDTight", "PFMETNoMu140_PFMHTNoMu140_IDTight"]
p=PostProcessor(".",files,cut=preselection,branchsel=None,modules=[TrigMETAnalysis(reference_paths,signal_paths)],noOut=True,histFileName="histos_METTrigNanoAOD_Muon_2022postEE.root",histDirName="metTrigAnalyzerNanoAOD")
p.run()
