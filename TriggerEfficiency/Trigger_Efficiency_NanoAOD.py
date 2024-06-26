#!/usr/bin/env python3
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module

#importing tools from nanoAOD processing set up to store the ratio histograms in a root file
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.examples.ttHTriggers_module import *

preselection=""
files=["/eos/cms/store/group/phys_higgs/moameen/tthmlep/NanoTrees_forCMGRDF_100524/2022EE/Muon_Run2022E.root",
       "/eos/cms/store/group/phys_higgs/moameen/tthmlep/NanoTrees_forCMGRDF_100524/2022EE/Muon_Run2022F.root",
       "/eos/cms/store/group/phys_higgs/moameen/tthmlep/NanoTrees_forCMGRDF_100524/2022EE/Muon_Run2022G.root",
       ]
reference_paths = ["PFMET120_PFMHT120_IDTight"]
signal_paths = ["Ele32_WPTight_Gsf", "IsoMu24", "IsoMu27", "PFMETTypeOne140_PFMHT140_IDTight", "Ele23_Ele12_CaloIdL_TrackIdL_IsoVL", "Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8", "Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ"]
p=PostProcessor(".",files,cut=preselection,branchsel=None,modules=[TrigAnalysis(reference_paths,signal_paths)],noOut=True,histFileName="histos_2lssTrig_data2022postEE_v1.root",histDirName="metTrigAnalyzerNanoAOD")
p.run()
