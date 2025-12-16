from machine import Pin, I2S # type:ignore (micropython lib)
from micropython import const #type:ignore 
from collections import deque
from bd_defs import *


NOT_ENOUGH_DATA = -1
NO_AUDIO_FOUND = -2

# Audio Sampling stuff:
NOISEFLOOR = const(300) # threshold from the mean that counts as actual audio
MIDPOINT = const(32768) # should be the middle point of a 16-bit audio packet???
BITRATE = const(8000) # 8K is what telephones used, so that should be good enough for me?
SAMPS_PER_BIT = const((BITRATE / 1000) * BIT_LENGTH)
# remember: I2S uses little-endian data!! 

class TDD_Interface:
    def __init__(self, rx_clock, rx_word_sel, rx_data, tx_clock, tx_word_sel, tx_data):
        self.audio_in = I2S(0, sck = Pin(rx_clock), ws = Pin(rx_word_sel), sd = Pin(rx_data), 
                       mode = I2S.RX,
                       bits = 16,
                       format = I2S.mono,
                       rate = BITRATE,
                       ibuf = BITRATE * 2 # 2 seconds of incoming data
                       )
        self.audio_out = I2S(1, sck = Pin(tx_clock), ws = Pin(tx_word_sel), sd = Pin(tx_data),
                             mode = I2S.TX,
                             bits = 16,
                             format = I2S.mono,
                             rate = BITRATE,
                             ibuf = BITRATE # 1 second should be more than enough for our output?
                             )
        self.in_audio_buff = bytearray()
        self.out_audio_buff = bytearray()
        self.in_data_buff = deque((), 255)
        self.out_data_buff = deque((), 255)
        self.busy = False # are we busy decoding or encoding data? 

    def decode_audio_buffer(self) -> int:
        ''' Decodes the incoming audio buffer'''
        last_tone = -1 # no previous tone at this point.
        # Trim until we hit the start of audio data:
        while True:
            if len(self.in_audio_buff) < 2:
                return NOT_ENOUGH_DATA
            sample = int.from_Bytes(self.in_audio_buff[0:2], 'little')
            if sample > NOISEFLOOR + MIDPOINT or sample < MIDPOINT - NOISEFLOOR:
                break
            self.in_audio_buff = self.in_audio_buff[2:] # snip until we get good data
        
        # Set up some counters for our next byte:
        buffbyte = 0
        bitcount = 0
        started_byte = False
        # Process our buffer until we no longer contain a full byte
        while len(self.in_audio_buff) > SAMPS_PER_BIT * 8:
            next_tone = get_tone_value(self.in_audio_buff[SAMPS_PER_BIT * bitcount:SAMPS_PER_BIT * bitcount + 1 ], last_tone)
            if next_tone < 0:
                last_tone = next_tone
                # snip our buffer by a bit to get a clean signal?
                self.in_audio_buff = self.in_audio_buff[SAMPS_PER_BIT / 4:]
                continue
            if not started_byte and next_tone == SPACE_FREQ:
                started_byte = True
                bitcount = 0
                buffbyte = 0
                while started_byte:
                        # rewrite our sampler but make it trim the ends!!!!!!
                    if started_byte and next_tone == MARK_FREQ: # start bit acquired, we're getting the mark tone
                        buffbyte |= (1 << bitcount)
                        bitcount += 1
                    elif started_byte and bitcount < 5: # it's a space frequency, but we're not ready for a stop bit
                        buffbyte |= (0 << bitcount)
                        bitcount += 1
                    elif started_byte and bitcount == 5 and next_tone == SPACE_FREQ:
                        bitcount += 1
                        last_tone = MARK_FREQ # ensure we treat a borderline as a space, since it probably will be one!
                        
                    elif started_byte and bitcount == 6 and next_tone == SPACE_FREQ:
                        self.in_data_buff.append(buffbyte)
                        started_byte = False
                    else:
                        print("I think this only happens when i mess up???")

            



            
                



def count_crossings(data:bytearray) -> int:
    count = 0
    firstbyte = int.frombytes(data[0:1], "little")
    data_size = len(data) # doing before the loop to avoid calling that every goddamn time
    if firstbyte > MIDPOINT:
        above = True
    else:
        above = False
    i = 0
    while i < data_size:
        if above & int.frombytes(data[i, i+1], "little") < MIDPOINT:
            count += 1
            above = False
        elif int.frombytes(data[i, i+1], "little") > MIDPOINT and not above:
            count += 1
            above = True
        i += 2
    return count

def get_tone_value(data_slice:list, last_tone = -1) -> int:
    '''Returns the value of the data slice given as either mark, space or invalid'''
    crosses = count_crossings(data_slice)
    if crosses < (MARK_RATE * BIT_LENGTH) - 2: # not enough crossings! Sample a bit later on.
        return INVALID_TONE
    elif crosses > (SPACE_RATE * BIT_LENGTH) + 3: 
        return INVALID_TONE # Probably picking up too much noise?
    elif crosses >= (MARK_RATE * BIT_LENGTH) and crosses < ((SPACE_RATE - .5) * BIT_LENGTH):
        return MARK_FREQ # most likely 1400 Hz
    elif crosses > ((MARK_RATE + .5) * BIT_LENGTH) and crosses <= (SPACE_RATE * BIT_LENGTH) + 3:
        return SPACE_FREQ # most likely 1800 Hz
    else: # The messy part, what to do in the border region!
        if last_tone == SPACE_FREQ: # If our last tone was space, let's assume we're picking up the last bit of that
            return MARK_FREQ
        else:
            return SPACE_FREQ # It's most likely an offset sample containing our space frequency.
    