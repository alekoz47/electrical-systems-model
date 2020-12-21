import csv
import pandas as pd
import numpy as np



class ship:
    # This class will hold all the principal particulars of a vessel
    principal_particulars = []

    def __init__(self, ship_file):
        self.set_attributes(ship_file)
        self.check_overdefined()
        self.set_unknown_attributes()
    
    def set_attributes(self, ship_file):
        # Opens CSV input file and makes each data point a class attribute
        with open(ship_file, encoding='utf-8-sig') as file:
            data = csv.DictReader(file)
            for line in data:
                self.principal_particulars.append(line)
        for key in self.principal_particulars:
            if key['Value'] == '':
                setattr(self, key['Characteristic'], key['Value'])
            else:
                setattr(self, key['Characteristic'], float(key['Value']))
                

    def check_overdefined(self):
        if self.Cb and self.V != '':
            print('Both Cb and Cp are defined. The vessel is overdefined')
        if self.Cp and self.Cm !='':
            print('Both Cp and Cm are defined. The vessel is overdefined')
    
    def check_underdefined(self):
        pass
            
        
    
    def set_unknown_attributes(self):
        self.T = (self.Tf + self.Ta) / 2
        
        if self.LWL == '':
            self.LWL = 1.05 * self.LBP
        
        # Calcultes Froude Number when given speed in knots and LWL in meters
        self.Fr_design = self.Vdesign *0.51444444 / (np.sqrt(9.81 * self.LWL))
        
        if self.Lcb == '':
            self.Lcb = -(0.44*self.Fr_design - 0.094)
            # Equation 50.3
            # Estimates optimal LCB location
            # Developed Guldhammer and Harvald (1974)
        
        if self.Cb == '':
            self.Cb = self.V / (self.LWL * self.B * self.T)

        if self.V == '':
            self.V = self.Cb * self.LWL * self.B * self.T
        
        if self.Cp == '' and self.Cm != '':
            self.Cp = self.Cb/self.Cm
            
        if self.Cp != '' and self.Cm == '':
            self.Cm = self.Cb/self.Cp
            
        if self.Cp == '' and self.Cm == '':
            self.Cm = 1 / (1+ (1-self.Cb) ** 3.5)
            # Equation 50.4
            # Regression equation on a graph by Jensen (1994)
            
        if self.Cwp == '':
            self.Cwp = 0.763 * (self.Cp + 0.34)
            # Equation 50.5
            # Estimates water plane coefficient before lines plan is complete
            # Method developed by Bertram and Wobig (1999)
            
            # TODO add a check to determine if ship is proper range
            # TODO add way to switch equation for containership
            # self.Cwp = 3.226 * (self.Cp - 0.36)
        
        # TODO try to estimate Cstern
        
        # TODO estimate Abt
        
        # TODO try to estimate At
        
        if self.S == '':
            # Equation 50.8
            # Updated equation for more accurate prediction of slender hull forms
            # Holtrop, 1988
            c23 = 0.453 + 0.4425*self.Cb - 0.2862*self.Cm -0.003467*self.B/self.T + 0.3696*self.Cwp
            self.S = self.LWL * (2*self.T + self.B)*np.sqrt(self.Cm) * (
                0.615989*c23 + 0.111439*self.Cm**3 + 0.00571110*self.Cstern + 0.245357*c23/self.Cm) + (
                    3.45538*self.At + self.Abt/self.Cb*(1.4660538 + 0.5839497/self.Cm))
        if self.Lr == '':
            self.Lr = self.LWL * (1-self.Cp + 0.06*self.Cp*self.Lcb / (4*self.Cp - 1))
            # TODO This matches the excel program right now, not the textbook
                    
        if self.ie == '':
            # returns entrance angle in degrees
            # Equation 50.10
            # Holtrop and Mennen (1982)
            a = (-1)*((self.LWL/self.B)**0.80856 * (1-self.Cwp)**0.30484 * 
                      (1-self.Cp-0.0225*self.Lcb)**0.6367) * (
                          (self.Lr/self.B)**0.34574) * (100*self.V/(self.LWL**3))**0.16302
            self.ie = 1 + 89 * np.exp(a)
            
        


class holtrop_analysis:
    # These class performs a holtrop resistance analysis
    # Using the method presented in The Fundamentals of Ship Hydrodynamics: Fluid Mechanics, Ship Resistance and Propulsion. First Edition by Lothar Birk    
    
    def __init__(self):
        pass
    
    def find_Re(self, ship, speed, viscosity=1.188*10**(-6)):
        # Default Viscosity taken at 15C for SW in m^2/s
        Vs = 0.514444 * speed # converts knots to m/s
        Re = Vs * ship.LWL / viscosity
        return Re
    
    def find_Fn(self, ship, speed):
        g = 9.81 # acceleration due to gravity in m/s^2
        Vs = 0.514444 * speed # converts knots to m/s
        Fn = Vs / np.sqrt(g*ship.LWL)
        return Fn
    
    def frictional_resistance(self, ship, speed, density=1025.9):
        # This method returns the Rf for the given ship and speed
        # Default density taken at 15C for SW in kg/m^3
        Re = self.find_Re(self, ship, speed)
        Cf = 0.075 / (np.log10(Re) - 2)**2
        Vs = 0.514444 * speed # converts knots to m/s
        
        # Estimating the form factor (k) for the vessel
        # Method developed by Holtrop, 1984
        
        # Equation 50.14
        c14 = 1 + 0.011*ship.Cstern
        
        # Equation 50.15
        k = -0.07 + 0.487118 * c14 * (ship.B/ship.LWL)**1.06806 * (
            (ship.T/ship.LWL)**0.46106 * (ship.LWL/ship.Lr)**0.121563) * (
                (ship.LWL**3/ship.V)**0.36486 * (1-ship.Cp)**(-0.604247))

        Rf = 0.5*density*(Vs**2)*ship.S*Cf*(1+k)
        return Rf
    
    def app_resistance(self, ship, speed):
        # TODO calculate appendage drag for real
        Rapp = 0
        return Rapp
    
    # TODO add in bow thruster opening
    def bt_resistance(self, ship, speed):
        # TODO calculate bow thruster resistance for real
        Rb = 0
        return Rb
    
    def wave_resistance(self, ship, speed):
        g = 9.81 # acceleration due to gravity in m/s^2
        density=1025.9 # density at 15C in kg/m^3
        Fn = self.find_Fn(self, ship, speed)
        
        # Calculating needed coefficients
        # Table 50.3 and Table 50.4
        # I know the order is weird, but it was how the book had it
        
        # Calculating c7
        if ship.B/ship.LWL <= 0.11:
            c7 = 0.229577*(ship.B/ship.LWL)**(1/3)  
        if ship.B/ship.LWL > 0.11 and ship.B/ship.LWL <= 0.25:
            c7 = ship.B/ship.LWL 
        if ship.B/ship.LWL > 0.25:
            c7 = 0.5 - 0.0625*ship.LWL/ship.B
            
        c1 = 2223105*(c7**3.78613)*((ship.T/ship.B)**1.07961)*((90-ship.ie)**(-1.37565))
        
        c3 = 0.56*ship.Abt**1.5/(ship.B*ship.T*(0.31*np.sqrt(ship.Abt)+ship.Tf-ship.hb)) 
        
        c2 = np.exp(-1.89*np.sqrt(c3))
        
        c5 = 1 - 0.8*ship.At/(ship.B*ship.T*ship.Cm)
        
        # Calculating c15
        if ship.LWL**3/ship.V <= 512:
            c15 = -1.69385
        if ship.LWL**3/ship.V > 512 and ship.LWL**3/ship.V <= 1726.91:
            c15 = -1.69385 + (ship.LWL/(ship.V**(1/3))-8)/2.36
        if ship.LWL**3/ship.V > 1726.91:
            c15 = 0
        
        # Calculating c16
        if ship.Cp <= 0.8:
            c16 = 8.07981*ship.Cp - 13.8673*ship.Cp**2 + 6.984388*ship.Cp**3
        if ship.Cp > 0.8:
            c16 = 1.73014-0.7067*ship.Cp
            
        d =-0.9
        
        if ship.LWL/ship.B <=12:
            Lambda = 1.446*ship.Cp - 0.03*ship.LWL/ship.B
        if ship.LWL/ship.B > 12:
            Lambda = 1.446*ship.Cp - 0.36
        
        m1 = 0.0140407*ship.LWL/ship.T - 1.75254*ship.V**(1/3)/ship.LWL - 4.79323*ship.B/ship.LWL - c16
        
        c17 = 6919.3*(ship.Cm**(-1.3346))*((ship.V/ship.LWL**3)**2.00977)*(ship.LWL/ship.B-2)**1.40692
        
        m3 = -7.2035*((ship.B/ship.LWL)**0.326869)*(ship.T/ship.B)**0.605375
        
        # TODO clean up the m4 stuff
        
        def Rwa(Fr):
            # Equation 50.20
            m4 = 0.4*c15*np.exp(-0.034*Fr**(-3.29))
            m2 = c15 * ship.Cp**2 * np.exp(-0.1/(Fr**2))
            
            
            Rwa = c1*c2*c5*density*g*ship.V*np.exp(m1*Fr**d+m4*np.cos(Lambda*Fr**(-2)))
            return Rwa
        def Rwb(Fr):
            # Equation 50.21
            m4 = 0.4*c15*np.exp(-0.034*Fr**(-3.29))
            Rwb = c17*c2*c5*density*g*ship.V*np.exp(m3*Fr**d+m4*np.cos(Lambda*Fr**(-2)))
            return Rwb
        
        # Equation 50.22
        # if statements for Fr ranges
        if Fn <= 0.4:
            Rw = Rwa(Fn)
            
        if Fn > 0.4 and Fn <= 0.55:
            Rw = Rwa(0.4) + (20*Fn-8)/3*(Rwb(0.55)-Rwa(0.4))
            
        if Fn > 0.55:
            Rw = Rwb(Fn)
            
        return Rw
    
    def bulb_resistance(self, ship, speed):
        # The results for this calc differ slightly from the excel but I think it is close enough
        Vs = 0.514444 * speed # converts knots to m/s
        g = 9.81 # acceleration due to gravity in m/s^2
        density=1025.9 # density at 15C in kg/m^3
        Fn = self.find_Fn(self, ship, speed)

        # Equation 50.23
        hf = ship.Cp*ship.Cm*(ship.B*ship.T/ship.LWL)*(136-316.3*Fn)*Fn**3
        if hf < -0.01*ship.LWL:
            hf = -0.01*ship.LWL
        
        # Equation 50.24
        # ie is in the deg right, I am pretty sure that is correct, but I am not sure
        hw = ship.ie * Vs**2 / (400 * g)
        if hw > 0.01*ship.LWL:
            hw = 0.01*ship.LWL
        
        # Equation 50.25
        Fr_i = Vs / np.sqrt(g*(ship.Tf-ship.hb-0.25*np.sqrt(ship.Abt)+hf+hw))

        # Equation 50.26
        Pb = 0.56 * np.sqrt(ship.Abt) / (ship.Tf - 1.5*ship.hb + hf)
        
        # Equation 50.27
        Rb = 0.11*density*g*np.sqrt(ship.Abt)**3*Fr_i**3/(1+Fr_i**2)*np.exp(-3*Pb**(-2))
        
        return Rb
    
    def transom_resistance(self, ship, speed):
        Vs = 0.514444 * speed # converts knots to m/s
        g = 9.81 # acceleration due to gravity in m/s^2
        density=1025.9 # density at 15C in kg/m^3

        # Equation 50.28
        Fr_T = Vs / np.sqrt(2*g*ship.At / (ship.B + ship.B*ship.Cwp))
    
        # Equation 50.29
        if Fr_T <= 5:
            c6 = 0.2*(1-0.2*Fr_T)
        if Fr_T > 5:
            c6 = 0
            
        Rtr = 0.5 * density * Vs**2 *ship.At * c6
        return Rtr
    
    # TODO Calculate correlation allowance resistance
    def corr_resistance(self, ship, speed):
        Vs = 0.514444 * speed # converts knots to m/s
        g = 9.81 # acceleration due to gravity in m/s^2
        density=1025.9 # density at 15C in kg/m^3
        
        # Equation 50.31
        if ship.Tf <= 0.04:
            c4 = ship.Tf / ship.LWL
        if ship.Tf > 0.04:
            c4 = 0.04
        
        # Table 50.3
        c3 = 0.56*ship.Abt**1.5/(ship.B*ship.T*(0.31*np.sqrt(ship.Abt)+ship.Tf-ship.hb)) 
        c2 = np.exp(-1.89*np.sqrt(c3))
        
        # Equation 50.32
        Ca = 0.00546*(ship.LWL+100)**(-0.16)-0.002+0.003*np.sqrt(ship.LWL/7.5)*ship.Cb**4*c2*(0.04-c4)
        print(Ca)
        # excel equation is different, I have no idea why
        
        # TODO add in roughness correction delta Ca, Equation 50.33
        
        # TODO add in surface area for appendages, need to add default value in the ship class
        Ra = 0.5*density*Vs**2*(Ca)*(ship.S)
        
        return Ra
        
            
    def air_resistance(self, ship, speed):
        # TODO Calculate air resistance for real
        Raa = 0
        return Raa
    
    def total_resistance(self, ship, speed):
        Rf = self.frictional_resistance(self, ship, speed) # This includes form factor
        Rapp = self.app_resistance(self, ship, speed)
        Ra = self.corr_resistance(self, ship, speed)
        Rw = self.wave_resistance(self, ship, speed)
        Rb = self.bulb_resistance(self, ship, speed)
        Rtr = self.transom_resistance(self, ship, speed)
        Raa = self.air_resistance(self, ship, speed)
        
        Rt = Rf + Rapp + Ra + Rw + Rb + Rtr + Raa
        
        return Rt
    
    
    # TODO Hull-propeller interaction for power estimate
    def estimate_wake_fraction(self, ship, speed):
        Vs = 0.514444 * speed # converts knots to m/s
        g = 9.81 # acceleration due to gravity in m/s^2
        density=1025.9 # density at 15C in kg/m^3
        
        Rf = self.frictional_resistance(self, ship, speed) # This includes form factor
        Rapp = self.app_resistance(self, ship, speed)
        Ra = self.corr_resistance(self, ship, speed)
        
        # Equation 50.37
        Cv = (Rf+Rapp+Ra) / (0.5*density*Vs**2*ship.S)
        # TODO add in appendage surface area
        
        # Table 50.5
        
        
    def estimate_thrust_deduction(self, ship, speed):
        pass
    
    def estimate_power(self, ship, speed):
        pass    
    
        
        
        
        

data_link = '../data/Holtrop_input.csv'
test_vessel = ship(data_link)

if test_vessel.Cb != '':
    print('It works!')

#print(test_vessel.Cb)
#print(test_vessel.V)
print(holtrop_analysis.frictional_resistance(holtrop_analysis, test_vessel, 22)/1000)
print(holtrop_analysis.wave_resistance(holtrop_analysis, test_vessel, 22)/1000)
print(holtrop_analysis.bulb_resistance(holtrop_analysis, test_vessel, 22)/1000)
print(holtrop_analysis.transom_resistance(holtrop_analysis, test_vessel, 22)/1000)
print(holtrop_analysis.corr_resistance(holtrop_analysis, test_vessel, 22)/1000)
print(holtrop_analysis.total_resistance(holtrop_analysis, test_vessel, 22)/1000)


#print(holtrop_analysis.principal_particulars)