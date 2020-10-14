
import numpy as np
import GA_module as ga

# Alternance des gènes
def sexyTime_first(p1,p2):
    gr2 = p1.gr2
    gr4 = p1.gr4
    gr6 = p1.gr6
    aav = p1.aav
    
    gr3_2 = p2.gr3
    gr5_2 = p2.gr5
    rdiff_2 = p2.dgr
    aar_2 = p2.aar
    
    p1.gr3 = gr3_2
    p1.gr5 = gr5_2
    p1.dgr = rdiff_2
    p1.aar = aar_2
    
    p2.gr2 = gr2
    p2.gr4 = gr4
    p2.gr6 = gr6
    p2.aav = aav

    
    return (p1, p2)
    

# Enfant maximum et enfant Minimum
def sexyTime_minmax(p1,p2):
    gear2ratio = find_big(p1.gr2, p2.gr2)
    gear3ratio = find_big(p1.gr3, p2.gr3)
    gear4ratio = find_big(p1.gr4, p2.gr4)
    gear5ratio = find_big(p1.gr5, p2.gr5)
    gear6ratio = find_big(p1.gr6, p2.gr6)
    reardifferentialratio = find_big(p1.dgr, p2.dgr)
    rearspoilerangle = find_big(p1.aav, p2.aav)
    frontspoilerangle = find_big(p1.aar, p2.aar)
    
    p1.gr2 = gear2ratio
    p1.gr3 = gear3ratio
    p1.gr4 = gear4ratio
    p1.gr5 = gear5ratio
    p1.gr6 = gear6ratio
    p1.dgr = reardifferentialratio
    p1.aav = rearspoilerangle
    p1.aar = frontspoilerangle
    
    gear2ratio = find_small(p1.gr2, p2.gr2)
    gear3ratio = find_small(p1.gr3, p2.gr3)
    gear4ratio = find_small(p1.gr4, p2.gr4)
    gear5ratio = find_small(p1.gr5, p2.gr5)
    gear6ratio = find_small(p1.gr6, p2.gr6)
    reardifferentialratio = find_small(p1.dgr, p2.dgr)
    rearspoilerangle = find_small(p1.aav, p2.aav)
    frontspoilerangle = find_small(p1.aar, p2.aar)
    
    p2.gr2 = gear2ratio
    p2.gr3 = gear3ratio
    p2.gr4 = gear4ratio
    p2.gr5 = gear5ratio
    p2.gr6 = gear6ratio
    p2.dgr = reardifferentialratio
    p2.aav = rearspoilerangle
    p2.aar = frontspoilerangle
    
def find_big(num1, num2):
    if (num1 >= num2):
        return num1
    else:
        return num2
    
def find_small(num1, num2):
    if (num1 <= num2):
        return num1
    else:
        return num2  
    
def sexyTime_5050(p1,p2):
    # Calculate new GearRatios
    p1.gr2, p2.gr2 = newGearRatio_5050(p1.gr2,p2.gr2)
    p1.gr3, p2.gr3 = newGearRatio_5050(p1.gr3,p2.gr3)
    p1.gr4, p2.gr4 = newGearRatio_5050(p1.gr4,p2.gr4)
    p1.gr5, p2.gr5 = newGearRatio_5050(p1.gr5,p2.gr5)
    p1.gr6, p2.gr6 = newGearRatio_5050(p1.gr6,p2.gr6)
    
    # Calculate new Differential Gear Ratio
    p1.dgr, p2.dgr = newDifferential_5050(p1.dgr, p2.dgr)
    
    # Calculate new fin angles
    p1.aar, p2.aar = newFinAngle_5050(p1.aar, p2.aar)
    p1.aav, p2.aav = newFinAngle_5050(p1.aav, p2.aav)  
    
def newGearRatio_5050(p1gr, p2gr):
    # Evaluate Gear Ratios in binary
    up1 = 56 & p1gr # 0b111000
    down1 = 7 & p1gr # 0b000111
    up2 = 56 & p2gr # 0b111000
    down2= 7 & p2gr # 0b000111
    # kids generation
    outp1gr = up1+down2
    outp2gr = up2+down1
    # Reavaluate for physical maximums
    if (outp1gr > 50):
        outp1gr = 50
    if (outp1gr < 1):
        outp1gr = 1
    if (outp2gr > 50):
        outp2gr = 50
    if (outp2gr < 1):
        outp2gr = 1
        
    return outp1gr, outp2gr 

def newDifferential_5050(p1dgr, p2dgr):
    # Evaluate Gear Ratios in binary
    up1 = 112 & p1dgr # 0b1110000
    down1 = 15 & p1dgr # 0b0001111
    up2 = 112 & p2dgr # 0b111000
    down2= 15 & p2dgr # 0b000111
    # kids generation
    outp1dgr = up1+down2
    outp2dgr = up2+down1
    # Reavaluate for physical maximums
    if (outp1dgr > 100):
        outp1dgr = 100
    if (outp1dgr < 10):
        outp1dgr = 10
    if (outp2dgr > 100):
        outp2dgr = 100
    if (outp2dgr < 10):
        outp2dgr = 10
        
    return outp1dgr, outp2dgr

def newFinAngle_5050(p1fin, p2fin):
    # Evaluate Fin angles in binary
    up1 = 992 & p1fin # 0b1110000
    down1 = 31 & p1fin # 0b0001111
    up2 = 992 & p2fin # 0b111000
    down2= 31 & p2fin # 0b000111
    # kids generation
    outp1fin = up1+down2
    outp2fin = up2+down1
    # Reavaluate for physical maximums
    if (outp1fin > 900):
        outp1fin = 900
    if (outp1fin < 0):
        outp1fin = 0
    if (outp2fin > 900):
        outp2fin = 900
    if (outp2fin < 0):
        outp2fin = 0
        
    return outp1fin, outp2fin