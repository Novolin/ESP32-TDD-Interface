# This is a test app for the goertzel algo stuff
from goertze import goertz
from bd_defs import *
from array import array
import wave

# establish our seeky dudes:
mark = goertz(MARK_FREQ, 10000)
space = goertz(SPACE_FREQ, 10000)

SAMPS_PER_BIT = 160 # how many samples in one millisecond
SAMPS_PER_BYTE = int(160 * 7.5)

def load_wav_data(filename) -> array:
    output = array("H")
    with wave.open(filename, 'r') as infile:
        if infile.getframerate() != 8000:
            print("Error! Wrong sample rate! needs 8KHz!")
            raise ValueError
        frames_read = 0
        while frames_read < infile.getnframes():
            output.append(int.from_bytes(infile.readframes(1)))
            frames_read += 1
    print("File data loaded!")
    return output

def find_bit_start(data) -> int:
    ''' returns the point where the start bit is first detected'''
    seek_point = 0
    while seek_point + SAMPS_PER_BIT < len(data):
        next_slice = data[seek_point:seek_point + SAMPS_PER_BIT]
        if space.calc(next_slice) > mark.calc(next_slice):
            print(f"Found start point! at data frame {seek_point}")
            return seek_point
        else:
            seek_point += 1
    print("Error: No start bit found?")
    return -1

def decode_byte(data_slice) -> int:
    ''' Decodes the byte from the audio given?'''
    outbyte = 0
    seek_pos = 0
    bitcount = 0
    while bitcount < 5:
        mark_val = mark.calc(data_slice[seek_pos:seek_pos + SAMPS_PER_BIT])
        space_val = space.calc(data_slice[seek_pos:seek_pos + SAMPS_PER_BIT])
        print(mark_val, space_val)
        if mark_val > space_val:
            outbyte |= 1 << bitcount
        bitcount += 1
        seek_pos += SAMPS_PER_BIT
    print(outbyte)
    return outbyte


# do the dang thing to start:
aud_data = load_wav_data('HELLO_50.wav')
start = find_bit_start(aud_data)

start_time = start / 8
print(f"Sample starts after {start_time} ms?")
audio_point = start
decoded = ""
while audio_point + SAMPS_PER_BYTE < len(aud_data):
    next_char = decode_byte(aud_data[audio_point:audio_point + SAMPS_PER_BYTE])
    decoded += LTRS[next_char]
    audio_point += SAMPS_PER_BYTE
print(decoded)