import os, sys
import ROOT

ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
import array

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

def conept_TTH(lep):
    if (abs(lep.pdgId)!=11 and abs(lep.pdgId)!=13): return lep.pt
    if (abs(lep.pdgId)==13 and lep.mediumId>0 and lep.mvaTTH > 0.85) or (abs(lep.pdgId) == 11 and lep.mvaTTH > 0.80): return lep.pt
    else: return 0.90 * lep.pt * (1 + lep.jetRelIso)

class TrigAnalysis(Module):
    def __init__(self, reference_paths, signal_paths):
        self.writeHistFile=True
        self.reference_paths=reference_paths
        self.signal_paths=signal_paths
        
    def beginJob(self,histFile=None,histDirName=None):
        Module.beginJob(self,histFile,histDirName)
        
        self.bins = {}
        self.bins["lep1_pt"] = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        self.bins["lep1_eta"] = [-2.4, -2.2, -2.0, -1.8, -1.6, -1.4, -1.2, -1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4]
        #self.bins["lep2_pt"] = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        
        self.h_passreftrig  = ROOT.TH1F("h_passreftrig" , "; passed ref trigger", 2, 0. , 2.)
        
        # pT of leading leptons
        self.h_lep1_pt_all = ROOT.TH1F("h_lep1_pt_all", "; Cone p_{T}^{\ell 1} [GeV]", len(self.bins["lep1_pt"])-1, array.array("d", self.bins["lep1_pt"]))
        self.h_lep1_pt_passed = ROOT.TH1F("h_lep1_pt_passed", "; Cone p_{T}^{\ell 1} [GeV];", len(self.bins["lep1_pt"])-1, array.array("d", self.bins["lep1_pt"]))
        self.h_lep1_pt_passedreftrig = ROOT.TH1F("h_lep1_pt_passedreftrig", "; Cone p_{T}^{\ell 1} [GeV];", len(self.bins["lep1_pt"])-1, array.array("d", self.bins["lep1_pt"]))
        self.h_lep1_pt_passedsignalANDreference = ROOT.TH1F("h_lep1_pt_passedsignalANDreference", "; Cone p_{T}^{\ell 1} [GeV];", len(self.bins["lep1_pt"])-1, array.array("d", self.bins["lep1_pt"]))
        # eta of leading leptons
        self.h_lep1_eta_all = ROOT.TH1F("h_lep1_eta_all", "; #eta (\ell 1)", len(self.bins["lep1_eta"])-1, array.array("d", self.bins["lep1_eta"]))
        self.h_lep1_eta_passed = ROOT.TH1F("h_lep1_eta_passed", "; #eta (\ell 1);", len(self.bins["lep1_eta"])-1, array.array("d", self.bins["lep1_eta"]))
        self.h_lep1_eta_passedreftrig = ROOT.TH1F("h_lep1_eta_passedreftrig", "; #eta (\ell 1);", len(self.bins["lep1_eta"])-1, array.array("d", self.bins["lep1_eta"]))
        self.h_lep1_eta_passedsignalANDreference = ROOT.TH1F("h_lep1_eta_passedsignalANDreference", "; #eta (\ell 1);", len(self.bins["lep1_eta"])-1, array.array("d", self.bins["lep1_eta"]))
        
        
        self.h_lep1_eta_vs_pt_all = ROOT.TH2F('h_lep1_eta_vs_pt_all', ';Cone p_{T}^{\ell 1} [GeV];#eta (\ell 1);', len(self.bins["lep1_pt"])-1,  array.array("d", self.bins["lep1_pt"]), len(self.bins["lep1_eta"])-1, array.array("d", self.bins["lep1_eta"]))
        self.h_lep1_eta_vs_pt_passed = ROOT.TH2F('h_lep1_eta_vs_pt_passed', ';Cone p_{T}^{\ell 1} [GeV];#eta (\ell 1);', len(self.bins["lep1_pt"])-1,  array.array("d", self.bins["lep1_pt"]), len(self.bins["lep1_eta"])-1, array.array("d", self.bins["lep1_eta"]))
        self.h_lep1_eta_vs_pt_passedreftrig = ROOT.TH2F('h_lep1_eta_vs_pt_passedreftrig', ';Cone p_{T}^{\ell 1} [GeV];#eta (\ell 1);', len(self.bins["lep1_pt"])-1,  array.array("d", self.bins["lep1_pt"]), len(self.bins["lep1_eta"])-1, array.array("d", self.bins["lep1_eta"]))
        self.h_lep1_eta_vs_pt_passedsignalANDreference = ROOT.TH2F('h_lep1_eta_vs_pt_passedsignalANDreference', ';Cone p_{T}^{\ell 1} [GeV];#eta (\ell 1);', len(self.bins["lep1_pt"])-1,  array.array("d", self.bins["lep1_pt"]), len(self.bins["lep1_eta"])-1, array.array("d", self.bins["lep1_eta"]))
        
        
        self.hList = {}
        for path in self.signal_paths:
            self.hList[f'h_lep1_pt_passtrig_HLT_{path}'] = ROOT.TH1F(f'h_lep1_pt_passtrig_HLT_{path}', ";p_{T}^{\ell 1} [GeV]", len(self.bins["lep1_pt"])-1, array.array("d", self.bins["lep1_pt"]))
            self.hList[f'h_lep1_eta_passtrig_HLT_{path}'] = ROOT.TH1F(f'h_lep1_eta_passtrig_HLT_{path}', ";#eta (\ell 1)", len(self.bins["lep1_eta"])-1, array.array("d", self.bins["lep1_eta"]))
            self.hList[f'h_lep1_eta_vs_pt_passtrig_HLT_{path}'] = ROOT.TH2F(f'h_lep1_eta_vs_pt_passtrig_HLT_{path}', ';Cone p_{T}^{\ell 1} [GeV];#eta (\ell 1)', len(self.bins["lep1_pt"])-1,  array.array("d", self.bins["lep1_pt"]), len(self.bins["lep1_eta"])-1, array.array("d", self.bins["lep1_eta"]))
        self.addObject(self.h_passreftrig )
        self.addObject(self.h_lep1_pt_all)
        self.addObject(self.h_lep1_pt_passed)
        self.addObject(self.h_lep1_pt_passedreftrig)
        self.addObject(self.h_lep1_pt_passedsignalANDreference)
        self.addObject(self.h_lep1_eta_all)
        self.addObject(self.h_lep1_eta_passed)
        self.addObject(self.h_lep1_eta_passedreftrig)
        self.addObject(self.h_lep1_eta_passedsignalANDreference)
        self.addObject(self.h_lep1_eta_vs_pt_all)
        self.addObject(self.h_lep1_eta_vs_pt_passed)
        self.addObject(self.h_lep1_eta_vs_pt_passedreftrig)
        self.addObject(self.h_lep1_eta_vs_pt_passedsignalANDreference)
        for h in self.hList:
            self.addObject(self.hList[h])

    def analyze(self, event):

        met = Object(event, "MET")
        hlt = Object(event, "HLT")
        
        # Check if event passes the reference trigger(s)
        refAccept=False
        for path in self.reference_paths:
            bit = getattr(hlt, path)
            if bit:
                refAccept = True
	
        # Save the bit of reference trigger and skim event
        self.h_passreftrig.Fill(refAccept)
        if not refAccept:
           return False
        
        # Require events to satisfy noise filters:
        met_filters = bool(
            event.Flag_goodVertices and
            event.Flag_globalSuperTightHalo2016Filter and
            event.Flag_HBHENoiseFilter and
            event.Flag_HBHENoiseIsoFilter and
            event.Flag_EcalDeadCellTriggerPrimitiveFilter and
            event.Flag_BadPFMuonFilter and
            event.Flag_BadPFMuonDzFilter and
            event.Flag_eeBadScFilter and
            event.Flag_ecalBadCalibFilter
        )
        if not met_filters:
            return False
        
        # Add any offline selection here:
        
        # MET    
        if event.MET_pt < 120:
            return False
          
        ## Leptons    
        leps = [l for l in Collection(event, 'LepGood') ]
        
        l1 = leps[0]
        l2 = leps[1]
        
        ret = [ 0 for l in leps ]
        if len(leps) == 2:
            for i,l1 in enumerate(leps):
                l2 = leps[1-i]
                if conept_TTH(l1) < 25 and conept_TTH(l2) < 15: continue 
                if l1.cutBased < 4 and l2.cutBased < 4: continue # (cutBased ID: 0:fail, 1:veto, 2:loose, 3:medium, 4:tight)
                ret[i] = 1      
        
        self.h_lep1_pt_all.Fill(conept_TTH(l1))
        self.h_lep1_eta_all.Fill(l1.eta)
        self.h_lep1_eta_vs_pt_all.Fill(conept_TTH(l1), l1.eta)
        
        # Check if event passes the signal trigger(s)
        signalOR = False
        for path in self.signal_paths:
            if getattr(hlt, path) == 1:
                signalOR = True
                self.hList[f'h_lep1_pt_passtrig_HLT_{path}'].Fill(conept_TTH(l1))
                self.hList[f'h_lep1_eta_passtrig_HLT_{path}'].Fill(l1.eta)
                self.hList[f'h_lep1_eta_vs_pt_passtrig_HLT_{path}'].Fill(conept_TTH(l1), l1.eta)

        if signalOR:
            self.h_lep1_pt_passed.Fill(conept_TTH(l1))
            self.h_lep1_eta_passed.Fill(l1.eta)
            self.h_lep1_eta_vs_pt_passed.Fill(conept_TTH(l1), l1.eta)
            
        if refAccept:
            self.h_lep1_pt_passedreftrig.Fill(conept_TTH(l1))
            self.h_lep1_eta_passedreftrig.Fill(l1.eta)
            self.h_lep1_eta_vs_pt_passedreftrig.Fill(conept_TTH(l1), l1.eta)
            
        if signalOR and hlt.PFMET120_PFMHT120_IDTight == 1: ## check if OR of signal_path(Trigger_2lss) and ref_path (Trigger_MET) are activated
            self.h_lep1_pt_passedsignalANDreference.Fill(conept_TTH(l1))
            self.h_lep1_eta_passedsignalANDreference.Fill(l1.eta)
            self.h_lep1_eta_vs_pt_passedsignalANDreference.Fill(conept_TTH(l1), l1.eta)    
            
        return True
