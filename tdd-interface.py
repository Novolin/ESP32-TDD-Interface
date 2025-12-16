from machine import Pin, I2S # type:ignore (micropython lib)
from micropython import const #type:ignore 
from collections import deque
import asyncio
from bd_defs import *


NOT_ENOUGH_DATA = -1
NO_AUDIO_FOUND = -2

# Audio Sampling stuff:
NOISEFLOOR = const(300) # threshold from the mean that counts as actual audio
MIDPOINT = const(32768) # should be the middle point of a 16-bit audio packet???
BITRATE = const(10000) # 10KHz should let me tell the diff easily, without too much overhead.
SAMPS_PER_BIT = const((BITRATE / 1000) * BIT_LENGTH)





class TDD_Rx:
    def __init__(self, clock, word_sel, serial_data):
        # Interface setup:
        self.clk = Pin(clock)
        self.ws = Pin(word_sel)
        self.sd = Pin(serial_data)
        self.interface = I2S(2, #type:ignore
            sck = self.clk, ws = self.ws, sd = self.sd
            mode = I2S.RX,
            bits = 16,
            format = I2S.mono
            rate = BITRATE,
            ibuf = BITRATE * 2) # 2s of buffered data, we should be able to decode that easily!!
        # Byte setup:
        self.audio_buffer = []
        self.data_buffer = deque()
    
    def decode_audio_buffer(self):
        '''Parses the audio data, adds it to the data buffer.'''

        # find the audio start point!
        aud_start = 0
        for i in range(len(self.audio_buffer)):
            if self.audio_buffer[i] > MIDPOINT + NOISEFLOOR or self.audio_buffer[i] < MIDPOINT - NOISEFLOOR:
                aud_start = i
                break # we're good!

        if len(self.audio_buffer[aud_start:]) < (BITRATE/1000) * (BIT_LENGTH * 7.5): # I know an audio signal will be 180ms long coming from the TDD. That's 7.5 bits in length.
            return NOT_ENOUGH_DATA # not enough audio data!
        

        # now sample until we know we get a SPACE tone!
        bitstarted = False
        start_time = aud_start
        while not bitstarted:
            if get_tone_value(self.audio_buffer[start_time:start_time + SAMPS_PER_BIT]) != 0:
                bitstarted += 2 



def count_crossings(data:list) -> int:
    count = 0
    if data[0] > MIDPOINT:
        above = True
    else:
        above = False
    for i in data:
        if above & i < MIDPOINT:
            count += 1
            above = False
        elif i > MIDPOINT and not above:
            count += 1
            above = True
    return count

def get_tone_value(data_slice:list):
    '''Returns the value of the data slice given as either mark, space or invalid'''
    crosses = count_crossings(data_slice)
