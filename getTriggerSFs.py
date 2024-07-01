import ROOT

class getTriggerSFs:
    def __init__(self):
        # Load the eff of TH1s
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
        # Ensure the pt is within the bin range
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
    
    # This is the SF for for 2lss_Trigger for each bin
    def getScaleFactors(self, bin_edges):
        scale_factors = []
        for i in range(len(bin_edges) - 1):
            bin_start = bin_edges[i]
            #print(bin_start)
            bin_end = bin_edges[i + 1]
            #print(bin_end)
            avg_pt = (bin_start + bin_end) / 2.0
            #print(avg_pt)
            effData = self.getEfficiencyData(avg_pt)
            print(" - DATA Efficiency = %f" % effData)
            effMC = self.getEfficiencyMC(avg_pt)
            print(" - MC Efficiency = %f" % effMC)
            sf = effData / effMC if effMC != 0 else 0
            scale_factors.append(sf)
            print(f"Bin [{bin_start}, {bin_end}]: Scale Factor: {sf}")
        return scale_factors

if __name__ == "__main__":
    # Initialize the class
    trigger_effs = getTriggerSFs()
    
    # Define the bin edges
    bin_edges = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    
    # Calculate scale factors for each bin
    scale_factors = trigger_effs.getScaleFactors(bin_edges)

