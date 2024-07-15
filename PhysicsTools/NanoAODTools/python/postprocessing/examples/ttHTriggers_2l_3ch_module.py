import os, sys
import ROOT

ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
import array

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

#ROOT.gROOT.ProcessLine(".L /eos/user/m/moameen/cmgrdf-prototype/TTHAnalysis/TTHcommon/functionsTTH.cc")

def conept_TTH(lep):
    if (abs(lep.pdgId)!=11 and abs(lep.pdgId)!=13): return lep.pt
    if (abs(lep.pdgId)==13 and lep.mediumId>0 and lep.mvaTTH > 0.85) or (abs(lep.pdgId) == 11 and lep.mvaTTH > 0.80): return lep.pt
    else: return 0.90 * lep.pt * (1 + lep.jetRelIso)

class TrigAnalysis(Module):
    def __init__(self, filename, channel):
        self.writeHistFile=True
        self.filename=filename
        self.cahnnel=channel

    def beginJob(self,histFile=None,histDirName=None):
        Module.beginJob(self,histFile,histDirName)
        
        self.bins = {}
        self.bins["lep1_pt"] = [20, 40, 50, 65, 80, 100, 200]
        self.bins["lep2_pt"] = [20, 40, 50, 65, 80, 100, 200]
        
        # l1
        self.h1_pre_l1pt = ROOT.TH1F("h1_pre_l1pt", "; Cone p_{T}^{\ell 1} [GeV];", len(self.bins["lep1_pt"])-1, array.array("d", self.bins["lep1_pt"]))
        self.h1_pre_l2pt = ROOT.TH1F("h1_pre_l2pt", "; Cone p_{T}^{\ell 2} [GeV];", len(self.bins["lep2_pt"])-1, array.array("d", self.bins["lep2_pt"]))
        
        # l2
        self.h1_l1pt = ROOT.TH1F("h1_l1pt", "; Cone p_{T}^{\ell 1} [GeV];", len(self.bins["lep1_pt"])-1, array.array("d", self.bins["lep1_pt"]))
        self.h1_l2pt = ROOT.TH1F("h1_l2pt", "; Cone p_{T}^{\ell 2} [GeV];", len(self.bins["lep2_pt"])-1, array.array("d", self.bins["lep2_pt"]))
        
        self.all_events1 = ROOT.TH1F('all_events1','lep_tag',1,0,1)
        self.all_events2 = ROOT.TH1F('all_events2','met_tag',1,0,1)
        self.all_events3 = ROOT.TH1F('all_events3','lepmet_tag',1,0,1)
        
        self.pass_lep_trigger= ROOT.TH1F('pass_lep_trigger','pass_lep_trigger',1,0,1)
        self.pass_met_trigger= ROOT.TH1F('pass_met_trigger','pass_met_trigger',1,0,1)
        self.pass_lepmet_trigger= ROOT.TH1F('pass_lepmet_trigger','pass_lepmet_trigger',1,0,1)
        
        # pT of sub-leading leptons (lep2)
        self.h_lep2_pt_all = ROOT.TH1F("h_lep2_pt_all", "; Cone p_{T}^{\ell 2} [GeV];Efficiency", len(self.bins["lep2_pt"])-1, array.array("d", self.bins["lep2_pt"]))
        self.h_lep2_pt = ROOT.TH1F("h_lep2_pt", "; Cone p_{T}^{\ell 2} [GeV];Efficiency", len(self.bins["lep2_pt"])-1, array.array("d", self.bins["lep2_pt"]))
        self.h_lep2_pt_passed = ROOT.TH1F("h_lep2_pt_passed", "; Cone p_{T}^{\ell 2} [GeV];Efficiency", len(self.bins["lep2_pt"])-1, array.array("d", self.bins["lep2_pt"]))
        self.h_lep2_pt_passedreftrig = ROOT.TH1F("h_lep2_pt_passedreftrig", "; Cone p_{T}^{\ell 2} [GeV];Efficiency", len(self.bins["lep2_pt"])-1, array.array("d", self.bins["lep2_pt"]))
        self.h_lep2_pt_passedsignalANDreference = ROOT.TH1F("h_lep2_pt_passedsignalANDreference", "; Cone p_{T}^{\ell 2} [GeV];Efficiency", len(self.bins["lep2_pt"])-1, array.array("d", self.bins["lep2_pt"]))
        

        self.addObject(self.h1_pre_l1pt)
        self.addObject(self.h1_pre_l2pt)
        
        self.addObject(self.h1_l1pt)
        self.addObject(self.h1_l2pt)
        
        self.addObject(self.all_events1)
        self.addObject(self.all_events2)
        self.addObject(self.all_events3)
        
        self.addObject(self.pass_lep_trigger)
        self.addObject(self.pass_met_trigger)
        self.addObject(self.pass_lepmet_trigger)

    def analyze(self, event):
        
        # Require events to satisfy noise filters:
        met_filters = bool(
            event.Flag_goodVertices and
            event.Flag_globalSuperTightHalo2016Filter and
            event.Flag_EcalDeadCellTriggerPrimitiveFilter and
            event.Flag_BadPFMuonFilter and
            event.Flag_BadPFMuonDzFilter and
            event.Flag_hfNoisyHitsFilter and
            event.Flag_eeBadScFilter and
            event.Flag_ecalBadCalibFilter
        )
        if not met_filters:
            return False
            
        ###### ee cahhhel ######
        if self.cahnnel == 'ee':  
            # Leptons    
            leps = [l for l in Collection(event, 'LepGood')]
        
            #leps = sorted(leps, key=lambda x: x.pt, reverse=False)
        
            if len(leps) < 2:
                return False
                
            id1,id2 = abs(leps[0].pdgId), abs(leps[1].pdgId)
            if not ((id1 == id2) and (id1 == 11)): 
                return False    
        
            l1, l2 = leps[0], leps[1]
        
            if self.filename =='TTto2L2Nu':
                #print('yes, weight is calculating for the MC file to apply')
                weight = event.prescaleFromSkim*event.puWeight
            else:
                weight = event.prescaleFromSkim
            #weight = event.prescaleFromSkim
        
            if conept_TTH(l1) < 25 and conept_TTH(l2) < 15:
                return False
        
            if event.MET_pt < 120:
                return False
            
            self.all_events1.Fill(0.99,weight)
            self.all_events2.Fill(0.99,weight)
            self.all_events3.Fill(0.99,weight)
        
            if (event.HLT_Ele32_WPTight_Gsf or event.HLT_Ele35_WPTight_Gsf or event.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL or event.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ):
                self.pass_lep_trigger.Fill(0.99,weight)
            
            if (event.HLT_PFMET120_PFMHT120_IDTight):
                self.pass_met_trigger.Fill(0.99,weight)
                self.h1_pre_l1pt.Fill(conept_TTH(l1),weight)
                self.h1_pre_l2pt.Fill(conept_TTH(l2),weight)
            
                if (event.HLT_Ele32_WPTight_Gsf or event.HLT_Ele35_WPTight_Gsf or event.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL or event.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ):
                    self.pass_lepmet_trigger.Fill(0.99,weight)
                    self.h1_l1pt.Fill(conept_TTH(l1),weight)
                    self.h1_l2pt.Fill(conept_TTH(l2),weight)
                    
        ###### em cahhhel ######
        if self.cahnnel == 'em':  
            # Leptons    
            leps = [l for l in Collection(event, 'LepGood')]
        
            #leps = sorted(leps, key=lambda x: x.pt, reverse=False)
        
            if len(leps) < 2:
                return False
                
            id1,id2 = abs(leps[0].pdgId), abs(leps[1].pdgId)
            if ((id1 == 11 and id2 == 13) or (id1 == 13 and id2 == 11)):
                return False    
        
            l1, l2 = leps[0], leps[1]
        
            if self.filename =='TTto2L2Nu':
                #print('yes, weight is calculating for the MC file to apply')
                weight = event.prescaleFromSkim*event.puWeight
            else:
                weight = event.prescaleFromSkim
            #weight = event.prescaleFromSkim
        
            if conept_TTH(l1) < 25 and conept_TTH(l2) < 15:
                return False
        
            if event.MET_pt < 120:
                return False
            
            self.all_events1.Fill(0.99,weight)
            self.all_events2.Fill(0.99,weight)
            self.all_events3.Fill(0.99,weight)

            if (event.HLT_IsoMu24 or event.HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL or event.HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ or event.HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ or event.HLT_Ele32_WPTight_Gsf):
                self.pass_lep_trigger.Fill(0.99,weight)
            
            if (event.HLT_PFMET120_PFMHT120_IDTight):
                self.pass_met_trigger.Fill(0.99,weight)
                self.h1_pre_l1pt.Fill(conept_TTH(l1),weight)
                self.h1_pre_l2pt.Fill(conept_TTH(l2),weight)
                
                if (event.HLT_IsoMu24 or event.HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL or event.HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ or event.HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ or event.HLT_Ele32_WPTight_Gsf):
                    self.pass_lepmet_trigger.Fill(0.99,weight)
                    self.h1_l1pt.Fill(conept_TTH(l1),weight)
                    self.h1_l2pt.Fill(conept_TTH(l2),weight)
                    
        ###### mm cahhhel ######
        if self.cahnnel == 'mm':  
            # Leptons    
            leps = [l for l in Collection(event, 'LepGood')]
        
            #leps = sorted(leps, key=lambda x: x.pt, reverse=False)
        
            if len(leps) < 2:
                return False
                
            id1,id2 = abs(leps[0].pdgId), abs(leps[1].pdgId)
            if ((id1 == id2) and (id1 == 13)):
                return False    
        
            l1, l2 = leps[0], leps[1]
        
            if self.filename =='TTto2L2Nu':
                #print('yes, weight is calculating for the MC file to apply')
                weight = event.prescaleFromSkim*event.puWeight
            else:
                weight = event.prescaleFromSkim
            #weight = event.prescaleFromSkim
        
            if conept_TTH(l1) < 25 and conept_TTH(l2) < 15:
                return False
        
            if event.MET_pt < 120:
                return False
            
            self.all_events1.Fill(0.99,weight)
            self.all_events2.Fill(0.99,weight)
            self.all_events3.Fill(0.99,weight)

            if (event.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8 or event.HLT_IsoMu24):
                self.pass_lep_trigger.Fill(0.99,weight)
            
            if (event.HLT_PFMET120_PFMHT120_IDTight):
                self.pass_met_trigger.Fill(0.99,weight)
                self.h1_pre_l1pt.Fill(conept_TTH(l1),weight)
                self.h1_pre_l2pt.Fill(conept_TTH(l2),weight)
                
                if (event.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8 or event.HLT_IsoMu24):
                    self.pass_lepmet_trigger.Fill(0.99,weight)
                    self.h1_l1pt.Fill(conept_TTH(l1),weight)
                    self.h1_l2pt.Fill(conept_TTH(l2),weight)

        return True
