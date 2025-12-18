# Attempting to do decoding using a goertzel algo
# insert hello.jpg joke here
# I don't understand how any of this math actually works,
# but I do know how the program flow from where i got this works.

# Try running with set sample data, e.g. a big ol list of premade samples?
from bd_defs import *
from math import cos, sin, pi
from cmath import polar


BITRATE = 11000 # 11kHz is a bit high, but more accurate.
SAMPS_PER_BIT = BITRATE/BIT_LENGTH # should be 220 for 50 baud, ~240 for 45.5. Don't use 45.5 if you can avoid it.

# Samples per cycle for each tone:
SPC_MARK = BITRATE / MARK_FREQ
SPC_SPACE = BITRATE/ SPACE_FREQ

# Omega values for each tone
w_mark = (2 * pi )/ SPC_MARK
w_space = (2* pi) / SPC_SPACE

