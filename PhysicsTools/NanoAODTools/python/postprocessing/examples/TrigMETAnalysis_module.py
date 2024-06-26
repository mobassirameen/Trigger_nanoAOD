import ROOT

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class TrigMETAnalysis(Module):
    def __init__(self, reference_paths, signal_paths):
        self.writeHistFile=True
        self.reference_paths=reference_paths
        self.signal_paths=signal_paths
        
    def beginJob(self,histFile=None,histDirName=None):
        Module.beginJob(self,histFile,histDirName)
        self.h_passreftrig  = ROOT.TH1F("h_passreftrig" , "; passed ref trigger", 2, 0. , 2.)
        self.h_met_all      = ROOT.TH1F("h_met_all" , "; E_{T}^{miss} [GeV]", 40, 100., 500.)
        self.h_met_passtrig = ROOT.TH1F("h_met_passtrig" , "; E_{T}^{miss} [GeV]", 40, 100., 500.)
        self.hList = []
        for path in self.signal_paths:
            histo = ROOT.TH1F("h_met_passtrig_HLT_%s" % (path), "; E_{T}^{miss} [GeV]", 40, 100., 500)
            self.hList.append(histo)
        self.addObject(self.h_passreftrig )
        self.addObject(self.h_met_all )
        self.addObject(self.h_met_passtrig )
        for h in self.hList:
            self.addObject(h)

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

        # Add any offline selection here:
        electrons = Collection(event, "Electron")
        nEle = 0
        for el in electrons:
            if abs(el.eta) > 2.4: continue
            if el.pt < 40: continue
            #if el.cutBased < 4: continue # (cutBased ID: 0:fail, 1:veto, 2:loose, 3:medium, 4:tight)
            nEle += 1

        # Keep only events with exactly one electron with pT > 40 GeV, tight ID
        if not (nEle == 1):
            return False
        
        self.h_met_all.Fill(met.pt)
        
        # Check if event passes the signal trigger(s)
        signalOR = False
        for path in self.signal_paths:
            bit = getattr(hlt, path)
            if bit:
                signalOR = True
                hist = next((h for h in self.hList if path in h.GetName()), None)
                hist.Fill(met.pt)

        if signalOR:
            self.h_met_passtrig.Fill(met.pt)

        return True
