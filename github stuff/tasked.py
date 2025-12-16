# trying non-blocking versions of i2s implementation?


from collections import deque
from machine import Pin, I2S #type:ignore
from micropython import const #type:ignore

MODE_IDLE = 0
MODE_CPU_RX = 1
MODE_CPU_TX = 2
MODE_TDD_RX = 3
MODE_TDD_TX = 4
curr_mode = -1 # boot mode


AUDIO_MIDPOINT = 32768 # half of a full 16-bit int
BIT_LENGTH = 20 # time in ms per bit. 20 for 50 baud, 22 for 45.5.
# Generate some audio samples:





class TDDInterface:
    def __init__(self, rx_clock, rx_word, rx_dat, tx_clock, tx_word, tx_dat, bit_length = 20):
        self.bit_length = bit_length # how many ms per bit
        self.rx = I2S(sck = rx_clock, ws = rx_word, sd = rx_dat,
                      mode=I2S.RX,
                      bits = 16,
                      format = I2S.MONO,
                      rate = 8000, # GOOD ENOUGH FOR MA BELL
                      ibuff = 16000 # 2s buffer?
                      )
        self.tx = I2S(sck = tx_clock, ws = tx_word, sd = tx_dat,
                      mode = I2S.TX,
                      bits = 16,
                      format = I2S.MONO,
                      rate = 8000, # Telephones dont need that much magic
                      ibuff = 8 * bit_length * 12 # effectively one byte at a time, with some breathing room
                      )
        self.in_buffer = deque((), 256)
        self.out_buffer = deque((), 256)
        self.tx_ready = False # when we are ready to send data, make this true
        # set up signal interrupts:
        self.tx.irq(self.tx_empty)
        
    
    def tx_empty(self):
        ''' Fills the TX buffer with the next byte of data, or silence'''
        if not self.tx_ready:
            signal = [AUDIO_MIDPOINT] * self.tx.ibuff
            self.tx.write(signal)
            return
        else:
            self.tx.write(self.generate_tone(self.out_buffer.popleft()))
    def generate_tone(self, data:int) -> list:
        '''Returns a list to write to the audio output'''
        output = []
        if self.out_buffer:
            next_byte = self.out_buffer.popleft()
        else:
            next_byte = [1400] * 10 # anti-echo, REPLACE WITH REAL!!!!
            self.tx_ready = False # flag our tx as complete.
        return output