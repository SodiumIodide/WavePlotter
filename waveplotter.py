#!/usr/bin/env python3

'''
Script to plot the sound waves of an audio file.
Relies on an installation of ffmpeg on the system path for the conversion
process to a .wav file.

Dependencies:
numpy for matrix modeling
matplotlib for graph output
wave for reading wav file information
os for file options
sys for exit calls
subprocess for call to ffmpeg
'''

import os
import sys
import subprocess
import wave
import numpy as np
import matplotlib.pyplot as plt

LINE_COLOR = 'black'
BG_COLOR = 'white'
RATIO = (13, 1)
LINEWIDTH = 0.005
DPI = 850
EXTENSIONS = ['wav',
              'mp1',
              'mp2',
              'mp3',
              'flac']

def convert(filename, channelprob=False):
    '''Converstion call to ffmpeg, relies on subprocess call to ffmpeg'''
    if not filename.endswith('.wav') or channelprob:
        new_filename = filename.split('.')[0] + '.wav'
        print("\nFile is not a .wav file, or is and has more than one channel.")
        print("If ffmpeg is not installed on system PATH, then please input")
        print("0 to kill this program now.")
        print("Otherwise, simply press Enter to run ffmpeg for conversion to a")
        print(".wav file:")
        result = input(">>> ")
        if '0' in result:
            sys.exit(1)
        try:
            args = ['ffmpeg', '-i', filename, '-ac', '1', new_filename]
            subprocess.check_call(args)
        except subprocess.CalledProcessError as err:
            print(err)
            sys.exit(1)
        print("Done")
        return new_filename
    else:
        return filename

def ensure_mono(filename):
    '''Ensure that the file is mono audio'''
    with wave.open(filename, 'r') as wavefile:
        num_channels = wavefile.getnchannels()
    if num_channels > 1:
        convert(filename, channelprob=True)

def read_wave(filename):
    '''Use wavefile to read in the data from a .wav file'''
    with wave.open(filename, 'r') as wavefile:
        num_chan = wavefile.getnchannels()
        num_frames = wavefile.getnframes()
        data_string = wavefile.readframes(num_chan * num_frames)
    wave_data = np.fromstring(data_string, np.int16)
    wave_data = np.reshape(wave_data, (-1, num_chan))
    return wave_data

def plot_wave(wave_data, fig_name):
    '''Create a matplotlib figure of the waveform'''
    max_wave = max(wave_data)
    # Normalize to limit computational time in matplotlib
    data = [d / max_wave for d in wave_data]
    plt.figure(figsize=RATIO, dpi=DPI, facecolor=BG_COLOR)
    plt.plot(data, LINE_COLOR, linewidth=LINEWIDTH)
    plt.axis('off')
    print("Showing plot. Modify and use GUI to save, or exit window to save")
    print("default settings to {}".format(fig_name))
    plt.savefig(fig_name, facecolor=BG_COLOR)
    plt.show()
    print("Plot saved to {}".format(fig_name))

def main():
    '''Main module of script'''
    files = [f for f in os.listdir('.') if f.split('.')[-1] in EXTENSIONS]
    filelist = {}
    for ind, file in enumerate(files):
        filelist[ind] = file
    print("List of files in directory:")
    for filenum in filelist:
        print("{0} - {1}".format(filenum, filelist[filenum]))
    print("Enter the number of the file")
    try:
        filename = filelist[int(input(">>> "))]
    except ValueError:
        print("Must be an integer number")
        raise ValueError
    print("Selected {}".format(filename))
    if filename.endswith('.wav'):
        ensure_mono(filename)
    else:
        filename = convert(filename)
    print("Processing...")
    wave_data = read_wave(filename)
    fig_name = filename.split('.')[0] + '.png'
    plot_wave(wave_data, fig_name)

if __name__ == '__main__':
    try:
        main()
    except ValueError:
        pass
    finally:
        print("\nProgram terminated\n")
