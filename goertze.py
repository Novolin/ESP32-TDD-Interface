# Attempting to do decoding using a goertzel algo
# insert hello.jpg joke here
# I don't understand how any of this math actually works,
# but I do know how the program flow from where i got this works.

# Try running with set sample data, e.g. a big ol list of premade samples?
from bd_defs import *
from math import cos, sin, pi
from cmath import polar


BITRATE = 11000 # 11kHz is a bit high, but more accurate.

class goertz:
    ''' A class to create an object you can use to target a specific frequency'''
    def __init__(self, target_freq):
        spc = BITRATE / target_freq 
        omega = 2 * pi / spc
        self.coeff = 2 * cos(omega)
        self.fac = -cos(omega) + 1j * sin(omega)
    
    def calc(self, dbuffer):
        ''' Calculates the magnitude of the frequency in the given # of samples'''
        q0 = q1 = q2 = 0
        for s in dbuffer:
            q0 = self.coeff * q1 - q2 + s
            q2 = q1
            q1 = q0
        return polar(q1 + q2 * self.fac)[0] / (len(dbuffer) / 2)


# TESTING TIME: ONLY USING THIS LIB BECAUSE I NEED IT TO DO THIS ON GITHUB AND NOT REAL H/W:

# Generate some known good waves:
SAMPS_PER_BIT = int((BITRATE / 1000) * BIT_LENGTH)
MIDPOINT = 32768
MARK_TABLE = []
SPACE_TABLE = []
dupes = 0
for i in range(SAMPS_PER_BIT):
    MARK_TABLE.append(int(MIDPOINT + (MIDPOINT * cos(2 * pi  * i*MARK_FREQ))))
    SPACE_TABLE.append(int(MIDPOINT + (MIDPOINT * sin(2 * pi * i *SPACE_FREQ))))
    if MARK_TABLE[0] == MARK_TABLE[i]:
        dupes += 1

print(MARK_TABLE[0], SPACE_TABLE[1])
print(dupes)
test_1400 = goertz(1400)
test_1800 = goertz(1800)

mark_test = test_1400.calc(MARK_TABLE)
mark_test_bad = test_1800.calc(MARK_TABLE)

space_test_bad = test_1400.calc(SPACE_TABLE)
space_test = test_1800.calc(SPACE_TABLE)

print(f"Mark test: {mark_test} for 1400 Hz, {mark_test_bad} for 1800\nSpace Test: {space_test_bad} for 1400, {space_test} for 1800.")