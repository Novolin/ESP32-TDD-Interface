# This file contains functions/definitions for baudot-related stuff

MARK_FREQ = 1400
SPACE_FREQ = 1800
BIT_LENGTH = 20 # bit length in ms. 20 = 50hz, 22 = 45.5
INVALID_TONE = -1
MARK_RATE = 2.8 # crossings per ms
SPACE_RATE = 3.6 # crossings per ms


LTRS = (
    "\b",
    "E",
    "\n",
    "A",
    " ",
    "S",
    "I",
    "U",
    "\r",
    "D",
    "R",
    "J",
    "N",
    "F",
    "C",
    "K",
    "T",
    "Z",
    "L",
    "W",
    "H",
    "Y",
    "P",
    "Q",
    "O",
    "B",
    "G",
    "FIGS",
    "M",
    "X",
    "V",
    "LTRS")
FIGS = (
    "\b",
    "3",
    "\n",
    "-",
    " ",
    "-",
    "8",
    "7",
    "\r",
    "$",
    "4",
    "'",
    ",",
    "!",
    ":",
    "(",
    "5",
    '"',
    ")",
    "2",
    "=",
    "6",
    "0",
    "1",
    "9",
    "?",
    "+",
    "FIGS",
    ".",
    "/",
    ";",
    "LTRS")

def sanitize_string(str_to_sani:str, replace_invalid:str = " ") -> str:
    outstring = ""
    for c in str_to_sani.upper(): # use the uppercase character set
        if c in LTRS or c in FIGS:
            outstring += c
        else:
            outstring += replace_invalid
    return outstring

def encode_string(string_to_encode:str) -> list:
    '''Encodes a string as a list of Baudot character #s, including character switches'''
    # ensure it's sanitized before we start!
    sani = sanitize_string(string_to_encode)
    outs = [31] # start with LTRS switch, per tdd standard
    curr_mode = LTRS
    for c in sani:
        if c in curr_mode:
            outs.append(curr_mode.index(c))
        elif curr_mode == LTRS:
            outs.append(27) # append FIGS switch
            curr_mode = FIGS
            outs.append(curr_mode.index(c))
        elif curr_mode == FIGS:
            outs.append(31) # append LTRS switch
            curr_mode = LTRS
            outs.append(curr_mode.index(c))
    return outs


