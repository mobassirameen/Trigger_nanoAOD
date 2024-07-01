import ROOT

class getTriggerSFs:
    def __init__(self):
        # Load the TH1s
        self.f_data = ROOT.TFile('/eos/user/m/moameen/Trigger_nanoAOD/efficiencies_2022_data.root', 'r')
        print("Reading the Data file", self.f_data)

        self.f_mc = ROOT.TFile('/eos/user/m/moameen/Trigger_nanoAOD/efficiencies_2022_mc.root', 'r')
        print("Reading the MC file", self.f_mc)
        
        self.lep2pTData = self.f_data.Get('lep2_pt_passedsignalANDreference_data')
        if not self.lep2pTData:
            raise ValueError("Histogram 'lep2_pt_passedsignalANDreference' not found in data file.")
        print("Data histogram loaded:", self.lep2pTData)
        
        self.lep2pTmc = self.f_mc.Get('lep2_pt_passedsignalANDreference_mc')
        if not self.lep2pTmc:
            raise ValueError("Histogram 'lep2_pt_passedsignalANDreference' not found in MC file.")
        print("MC histogram loaded:", self.lep2pTmc)
    
    def ptCheck(self, pt):
        if pt > 100:
            pt = 100
        elif pt < 10:
            pt = 10
        return pt
    
    def getEfficiency(self, effHist, pt):
        pt = self.ptCheck(pt)
        bin_number = effHist.FindBin(pt)
        eff = effHist.GetBinContent(bin_number)
        if eff > 1.:
            eff = 1
        return eff
    
    # This is the efficiency of lep2 from Data
    def getEfficiencyData(self, pt):
        return self.getEfficiency(self.lep2pTData, pt)
    
    # This is the efficiency of lep2 from MC
    def getEfficiencyMC(self, pt):
        return self.getEfficiency(self.lep2pTmc, pt)
    
    # This is the SF for for 2lss_Trigger
    def getScaleFactor(self, pt):
        effData = self.getEfficiencyData(pt)
        effMC = self.getEfficiencyMC(pt)
        sf = effData / effMC if effMC != 0 else 0
        return sf

if __name__ == "__main__":
    # Initialize the class
    trigger_effs = getTriggerSFs()
    
    # Example pt value to calculate the scale factor
    pt_value = 55  # Replace this with the actual pt value you want to check
    scale_factor = trigger_effs.getScaleFactor(pt_value)
    print("Scale Factor:", scale_factor)

