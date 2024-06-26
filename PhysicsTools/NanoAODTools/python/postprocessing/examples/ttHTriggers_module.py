import os
import ROOT

ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module

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
        self.h_passreftrig  = ROOT.TH1F("h_passreftrig" , "; passed ref trigger", 2, 0. , 2.)
        self.h_Lleptons_cut      = ROOT.TH1F("h_Lleptons_cut" , "; p_{T} [GeV]", 40, 30., 120.)
        self.h_Sleptons_cut      = ROOT.TH1F("h_Sleptons_cut" , "; p_{T} [GeV]", 40, 30., 120.)
        self.h_Lleptons_all      = ROOT.TH1F("h_Lleptons_all" , "; p_{T} [GeV]", 40, 30., 120.)
        self.h_Sleptons_all      = ROOT.TH1F("h_Sleptons_all" , "; p_{T} [GeV]", 40, 30., 120.)
        self.h_Lleptons_passtrig = ROOT.TH1F("h_Lleptons_passtrig" , "; p_{T} [GeV]", 40, 30., 120.)
        self.h_Sleptons_passtrig = ROOT.TH1F("h_Sleptons_passtrig" , "; p_{T} [GeV]", 40, 30., 120.)
        self.hList_ll = []
        self.hList_sl = []
        for path in self.signal_paths:
            histo_ll = ROOT.TH1F("h_Lleptons_passtrig_HLT_%s" % (path), "; p_{T} [GeV]", 40, 30., 120.)
            histo_sl = ROOT.TH1F("h_Sleptons_passtrig_HLT_%s" % (path), "; p_{T} [GeV]", 40, 30., 120.)
            self.hList_ll.append(histo_ll)
            self.hList_sl.append(histo_sl)
        self.addObject(self.h_passreftrig )
        self.addObject(self.h_Lleptons_cut )
        self.addObject(self.h_Sleptons_cut )
        self.addObject(self.h_Lleptons_all )
        self.addObject(self.h_Sleptons_all )
        self.addObject(self.h_Lleptons_passtrig )
        self.addObject(self.h_Sleptons_passtrig )
        for hll in self.hList_ll:
            self.addObject(hll)
        for hsl in self.hList_sl:
            self.addObject(hsl)

    def analyze(self, event):

        #met = Object(event, "MET") 
        
        hlt = Object(event, "HLT")
        flg = Object(event, "Flag")
        
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
           
        #****************************************************
        # Add any offline selection here:
        #****************************************************
        
        # check if event passes the filters
        falgfilterPassed=False
        for flag in ["goodVertices", "globalSuperTightHalo2016Filter"]:
            flagfilterbit = getattr(flg, flag)
            if flagfilterbit:
                flagfilterPassed=True
                #print("flags are applied*******")
            if not flagfilterPassed:
                return False
        ## MET    
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
                self.h_Lleptons_all.Fill(l1.pt) ## This will give all leading leptons before cuts
                self.h_Sleptons_all.Fill(l2.pt) ## This will give all sub-leading leptons before cuts
                if l1.cutBased < 4 and l2.cutBased < 4: continue # (cutBased ID: 0:fail, 1:veto, 2:loose, 3:medium, 4:tight)
                if conept_TTH(l1) < 25 and conept_TTH(l2) < 15: continue
                #print(l1.pt)
                #print(l2.pt)
                #print(100*"#")    
                ret[i] = 1
                self.h_Lleptons_cut.Fill(l1.pt) ## This will give the all leading leptons after cutse
                self.h_Sleptons_cut.Fill(l2.pt) ## This will give the all sub-leading leptons after cutse      
        
        # Check if event passes the signal trigger(s)
        signalOR = False
        for path in self.signal_paths:
            #pass
            bit = getattr(hlt, path)
            if bit:
                signalOR = True
                histll = next((h for h in self.hList_ll if path in h.GetName()), None)
                histsl = next((h for h in self.hList_sl if path in h.GetName()), None)
                histll.Fill(l1.pt)
                histsl.Fill(l2.pt)

        if signalOR and refAccept: ## check if OR of signal_pat and ref_path are activated
            self.h_Lleptons_passtrig.Fill(l1.pt)
            self.h_Sleptons_passtrig.Fill(l2.pt)

        return True
