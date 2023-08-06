#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Tue Jun  1 11:58:40 2021

@author: Fuh-Cherng Jeng

File name: fuhFunctions.py   

Purpose: Centralize functions, classes, etc. that are commonly used in AEP (Auditory ElectroPyshiology) Lab

2021-06-01 (v0.01)
    - add a class: File
    - add convert_softwareversion()
    - add readhear()
'''

# --- Construct a DataFrame from a Python built-in class: dataclasses, dataclass() ---
# This dataclass() function is a decorator that is used to add generated special methods to classes.
# Here, we create a new class 'File' (based on the Python built-in 'dataclass' class), with the following fields:
from dataclasses import dataclass       # The 'dataclasses' is a Python built-in module, for people to create classes of their own. From there, import only the dataclass() method. See 'https://docs.python.org/3/library/dataclasses.html' for details about the 'dataclasses' class in Python
@dataclass
class File:
    '''A class for keeping track of files and column parameters (par)'''
    directory: str
    subjectCode: str
    sessionNumber: int
    experimentString: str
    fileNumberString: str
    lexicalTone: int
    groupString: str
    stimToken: str
    nRepetitions: int
    si: float
    dBSPL: float
    labviewIndex: int
    headerIndex: int
    nChans: int

# define a dictionary for converting software version to string (in categories)
dict_softwareversion = {
    2.27: 'v2.26+',
    2.26: 'v2.26+',
    2.25: 'v2.17+',
    2.24: 'v2.17+',
    2.23: 'v2.17+',
    2.22: 'v2.17+',
    2.21: 'v2.17+',
    2.2:  'v2.17+',
    2.19: 'v2.17+',
    2.18: 'v2.17+',
    2.17: 'v2.17+',
    }

# read header v2.26
def readheader(fileToOpen):
    ''''
    --- Read header ---
    2021-06-01 (v01) 
        - program created by Fuh-Cherng Jeng
        - read header from data files (e.g., Sub001ses1_001.ss or Sub001ses1_001.avg) that are recorded using custom-made LabVIEW programs
        - header is a dictionary, with 81 key-value pairs
        - The header key values are not flatenned to DBL. That is, key values is a numpy array containing different data types
        - For clarity and trans-platform, use 'uint8' instead of 'char'
        - when reading a length indicator of a char array, use 'uint32' (instead of 4 uint8 numbers) 
        - This script works for both .ss and .avg files.
        - This script works for AEP v2.26+ (i.e., the LabVIEW AEP system in my lab)
        
    - To-Do:    
        - #TODO This script works for readheader217(), readheader224(), etc.
    
    ***IMPORTANT NOTE***
        - The data file doe NOT have be open by using fopen(), because the numpy fromfile() will simply read data without opening the file.
    
    --- INPUT ---
        - fileToOpen: filename (including filepath) of the data file 
            - The filename can be a string literal or a pathlib Path object
    
    --- OUTPUT ---
        - (header, nBytes): a tuple
            - header: a dictionary containing 81 key-value pairs. 
            - nBytes: a Python integer (int64)
    '''
    
    import numpy as np
    
    # Store header keys in a tuple
    keys = ('header_size',              #  0  [deafult: 81]
            'softwareversion',          #  1  [default: 2.27]
            'reserved02',               #  2  [default: 0]
            'reserved03',               #  3  [default: 0]    
            'reserved04',               #  4  [default: 0]
            'reserved05',               #  5  [default: 0]    
            'reserved06',               #  6  [default: 0]    
            'reserved07',               #  7  [default: 0]    
            'reserved08',               #  8  [default: 0]    
            'reserved09',               #  9  [default: 0]    
            'reserved10',               # 10  [default: 0] 
            'AO_nchannels',             # 11  [default: 2]
            'AO_samplingRate',          # 12  [default: 40000]
            'AO_silentInterval',        # 13  [default: 45] ms
            'AO0_dBSPL',                # 14  [default: 70] dB SPL
            'AO1_trigger_amp',          # 15  [default: 5] V
            'AO_nSamplesPerChannel',    # 16  [default: 15600]
            'AO_stim_max',              # 17  [default: 5] V
            'AO_stim_min',              # 18  [default: -5] V
            'stim_ear',                 # 19  [default: 1] 0 left, 1 right, 2 both
            'stim_type',                # 20  [default: 0] 0 waveFile, 1 clicks, 2 noise
            'stim_rate',                # 21  [default: 27.3]
            'AO0_amp_for_clicks',       # 22  [default: 5] V
            'AO0_pulseWidth',           # 23  [default: 0.1] ms
            'stim_polarity',            # 24  [default: 2] 0 original, 1 inverted, 2 alternating
            'AO0_stimPath',             # 25  [default: 'C\Stim2\RecordedToneStimlui\i\origcycN_150ms\i2_150ms.wav'] 
            'AO1_stimPath',             # 26  [default: 'C\Stim2\RecordedToneStimlui\i\origcycN_150ms\i2_150ms.wav'] 
            'AO1_stimType',             # 27  [default: 0] 0 trigger pulses, 1 original ao1 waveform, 2 inverted ao1 waveform, 3 continuous white noise
            'reserved28',               # 28  [default: 0]
            'reserved29',               # 29  [default: 0]
            'reserved30',               # 30  [default: 0]
            'AI_nchannels',             # 31  [default: 1]
            'AI_samplingRate',          # 32  [default: 20000]
            'AI_gain',                  # 33  [default: 50] k
            'AI_filter_1stNumber',      # 34  [default: 10] Hz
            'AI_filter_2ndNumber',      # 35  [default: 3000] Hz
            'AI_nsweepsAccepted',       # 36  [default: 0]
            'AI_nsweepsRejected',       # 37  [default: 0]
            'AI_max_nsweeps_accepted',  # 38  [default: 3002]
            'AI_art_rej_channel',       # 39  [default: 0]
            'AI_art_rej_criterion',     # 40  [default: 25] uV
            'AI_nsamplesReadPerChannel',# 41  [default: 7800]
            'AI_terminalConfiguration', # 42  [default: 10106] -1 default, 10083 RSE, 10078 NRSE, 10106 differential, 12529 Pesudodifferential
            'AI_max',                   # 43  [default: 10] V
            'AI_min',                   # 44  [default: -10] V
            'AI_timeIntervalToSave',    # 45  [default: 390] ms
            'AI_dateString',            # 46  [default: '12/21/2010']
            'AI_timeString',            # 47  [default: '11:28:03 AM']
            'reserved48',               # 48  [default: 0]
            'reserved49',               # 49  [default: 0]
            'reserved50',               # 50  [default: 0]
            'age_years',                # 51  [default: 99] years
            'gender',                   # 52  [default: 1] 0 Female, 1 Male
            'head_circumference',       # 53  [default: 99.0] cm
            'dominant_hand',            # 54  [default: 1] 0 Left, 1 Right
            'age_months',               # 55  [default: 0] months
            'age_days',                 # 56  [default: 0] days
            'native_language',          # 57  [default: 1] 0 English, 1 Chinese
            'notes',                    # 58  [default: 'delete this sentence and write your notes here...']
            'reserved59',               # 59  [default: 0]
            'reserved60',               # 60  [default: 0]
            'reserved61',               # 61  [default: 0]
            'reserved62',               # 62  [default: 0]
            'reserved63',               # 63  [default: 0]
            'reserved64',               # 64  [default: 0]
            'reserved65',               # 65  [default: 0]
            'reserved66',               # 66  [default: 0]
            'reserved67',               # 67  [default: 0]
            'reserved68',               # 68  [default: 0]
            'reserved69',               # 69  [default: 0]
            'reserved70',               # 70  [default: 0]
            'save_avg_flag',            # 71  [default: 1] 0 No, 1 Yes
            'save_ss_flag',             # 72  [default: 1] 0 No, 1 Yes
            'base_line_correction',     # 73  [default: 1] 0 No, 1 Yes
            'reserved74',               # 74  [default: 0]
            'reserved75',               # 75  [default: 0]
            'reserved76',               # 76  [default: 0]
            'reserved77',               # 77  [default: 0]
            'reserved78',               # 78  [default: 0]
            'reserved79',               # 79  [default: 0]
            'tail_flag'                 # 80  [default: 1] 0 No, 1 Yes
            )
      
    nBytes = 0                              # number of Bytes that have been read from the data file (i.e., current file position in bytes ==> i.e., offset)
    
    # element 0 (header_size)
    header_size = int(np.fromfile(fileToOpen, dtype=np.float64, count=1, offset=nBytes))
    nBytes += 8                             # increment nBytes
    
    # create a 1D numpy array to store values for the header dictionary
    values = np.full(header_size, None)     
    values[0] = header_size
    
    # element 1 (software version)
    values[1] = np.fromfile(fileToOpen, dtype=np.float64, count=1, offset=nBytes)[0]
    nBytes += 8
    
    # elements 2 to 24
    values[2:25] = np.fromfile(fileToOpen, dtype=np.float64, count=23, offset=nBytes)
    nBytes += 8 * (25 - 2)
    
    # element 25 (filepath\filename of the stimulus channel ao0)
    # NOTE: In LabVIEW, the length of a string is indicated by an uint32. >> That is, in LabVIEW, the structure of a string contains (1) a length indicator and (2) the actual char array. Note there is no ending char(0) at the end of a string, because we already have a length indicator in the beginning. >> So, let's read in the length indicator first, which is composed of an uint32. 
    # NOTE: We read in unit8 numbers and output them as ASCII characters, and do that for len times. % NOTE: '*char' is the same as 'uint8=>char', which means to read in an uint8 and output it as a char. >> Do that for len times. >> Thus, the output is a char array. >> Also, I MUST transpose the char array, so that all chars are displayed in one row. ==> So, these chars appear like a string in one line.
    len25 = np.fromfile(fileToOpen, dtype=np.uint32, count=1, offset=nBytes)[0]  # get length of element 25
    nBytes += 4
    
    a = np.fromfile(fileToOpen, dtype=np.uint8, count=len25, offset=nBytes)  # get element 25, as a list of ASCII values
    nBytes += len25
    values[25] = ''.join(map(chr, a))                 # convert a list of ASCII values to a string, by using the string.join() method, and the map() function
    
    # element 26 (filepath\filename of the stimulus channel ao1)
    len26 = np.fromfile(fileToOpen, dtype=np.uint32, count=1, offset=nBytes)[0]  # get length of element 26
    nBytes += 4
    
    a = np.fromfile(fileToOpen, dtype=np.uint8, count=len26, offset=nBytes)  # get element 26, as a list of ASCII values
    nBytes += len26
    values[26] = ''.join(map(chr, a))                 # convert a list of ASCII values to a string, by using the string.join() method, and the map() function
    
    # elements 27 to 45
    values[27:46] = np.fromfile(fileToOpen, dtype=np.float64, count=19, offset=nBytes)
    nBytes += 8 * (46 - 27)
    
    # element 46 (date stamp). Date stamp is just a char array, led by a length indicator. Each char is an uint8. The length indicator is composed of an uint32.
    len46 = np.fromfile(fileToOpen, dtype=np.uint32, count=1, offset=nBytes)[0]  # get length of element 46
    nBytes += 4
    
    a = np.fromfile(fileToOpen, dtype=np.uint8, count=len46, offset=nBytes)  # get element 46, as a list of ASCII values
    nBytes += len46
    values[46] = ''.join(map(chr, a))                 # convert a list of ASCII values to a string, by using the string.join() method, and the map() function
    
    # element 47 (time stamp). Time stamp is just a char array.
    len47 = np.fromfile(fileToOpen, dtype=np.uint32, count=1, offset=nBytes)[0]  # get length of element 47
    nBytes += 4
    
    a = np.fromfile(fileToOpen, dtype=np.uint8, count=len47, offset=nBytes)  # get element 47, as a list of ASCII values
    nBytes += len47
    values[47] = ''.join(map(chr, a))                 # convert a list of ASCII values to a string, by using the string.join() method, and the map() function
    
    # elements 48 to 57
    values[48:58] = np.fromfile(fileToOpen, dtype=np.float64, count=10, offset=nBytes)
    nBytes += 8 * (58 - 48)
    
    # element 58 (notes)
    len58 = np.fromfile(fileToOpen, dtype=np.uint32, count=1, offset=nBytes)[0]  # get length of element 58
    nBytes += 4
    
    a = np.fromfile(fileToOpen, dtype=np.uint8, count=len58, offset=nBytes)      # get element 58, as a list of ASCII values
    nBytes += len58
    values[58] = ''.join(map(chr, a))                 # convert a list of ASCII values to a string, by using the string.join() method, and the map() function
    
    # elements 59 to end
    n = header_size - 59
    values[59:header_size] = np.fromfile(fileToOpen, dtype=np.float64, count=n, offset=nBytes)
    nBytes += 8 * (header_size - 59)
                
    header = dict(zip(keys, values))                  # Get pairs of elements by using zip(), and then convert to a dictionary by using dict()

    return (header, nBytes)
    

# This is a dummy function for testing/debugging only. <== can be deleted/updated later...
def addTwo(x):
    return x + 2

 
   