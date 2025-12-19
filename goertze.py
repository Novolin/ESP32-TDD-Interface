# Attempting to do decoding using a goertzel algo
# insert hello.jpg joke here
# I don't understand how any of this math actually works,
# but I do know how the program flow from where i got this works.

# Try running with set sample data, e.g. a big ol list of premade samples?
from bd_defs import *
from math import cos, sin, pi
from cmath import polar


BITRATE = 8000 # 8kHz actually works better than other sample rates!

class goertz:
    ''' A class to create an object you can use to target a specific frequency'''
    def __init__(self, target_freq):
        spc = BITRATE / target_freq 
        omega = 2.0 * pi / spc
        self.coeff = 2.0 * cos(omega)
        self.fac = -cos(omega) + 1j * sin(omega)
    
    def calc(self, dbuffer):
        ''' Calculates the magnitude of the frequency in the given # of samples'''
        q0 = q1 = q2 = 0
        for s in dbuffer:
            q0 = self.coeff * q1 - q2 + s
            q2 = q1
            q1 = q0
        return polar(q1 + q2 * self.fac)[0] / (len(dbuffer) / 2)
