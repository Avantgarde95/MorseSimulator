''' Data load / Calculation '''

from __future__ import with_statement
import sys
import os
import json

path_core = os.path.dirname(os.path.abspath(__file__))
path_data = os.path.join(path_core, '../data/codetable.json')

try:
    with open(path_data, 'r') as p:
        codetable = json.load(p)
except IOError:
    print '[Error] Failed to load the data!'
    sys.exit(0)

table_chars, table_codes = zip(*sorted(codetable.items(),
                                       key = lambda x: len(x[1]),
                                       reverse = True))

codesize_min = min(len(c) for c in table_codes)
codesize_max = max(len(c) for c in table_codes)

def separate_samples(samples, num = 2):
    ''' Separate the samples into 'num' number of groups,
    and return the appropriate boundaries between groups (called
    'seperators').
    '''
    samples_sorted = sorted(samples)
    
    diffs = [samples_sorted[i+1] - samples_sorted[i]
             for i in xrange(len(samples_sorted)-1)]
    
    seps = [samples_sorted[0] + d
            for d in sorted(diffs)[-num+1:]]
    
    return seps

def guess_char(code):
    ''' Find the character matching the given (binary) code;
    If it doesn't exist, return '?'.
    '''
    if len(code) > codesize_max:
        code = code[:codesize_max]

    try:
        i = table_codes.index(code)
    except ValueError:
        return '?'

    return table_chars[i]

def decode_signals(signals):
    ''' Decode the signals and find the original message. '''
    num_signals = len(signals)

    # separate dit / dah
    times_on = [y - x for x, y in signals]
    seps_on = separate_samples(times_on, 2)
    
    if len(seps_on) >= 1:
        sep_dit_dah = seps_on[0]
    else:
        sep_dit_dah = max(times_on)

    print '[Log] Boundary between dit and dah :', sep_dit_dah
    
    # separate the gaps
    times_off = [signals[i+1][0] - signals[i][1]
                 for i in xrange(num_signals-1)]
    seps_off = separate_samples(times_off, 3)
    
    if len(seps_off) >= 2:
        sep_elem_char, sep_char_word = seps_off
    else:
        sep_elem_char = max(times_off)
        sep_char_word = sep_elem_char

    print '[Log] Boundary between elem. and char. :', sep_elem_char
    print '[Log] Boundary between char. and word. :', sep_char_word

    # encode the signals into a sequence
    sequence = ''

    for i in xrange(num_signals-1):
        if times_on[i] <= sep_dit_dah:
            sequence += '0' # dit
        else:
            sequence += '1' # dah

        if times_off[i] <= sep_elem_char:
            sequence += '2' # gaps between elements
        elif times_off[i] <= sep_char_word:
            sequence += '3' # gaps between characters
        else:
            sequence += '4' # gaps between words

    if times_on[-1] <= sep_dit_dah:
        sequence += '0'
    else:
        sequence += '1'

    print '[Log] Encoded the signals into'\
            ' the following sequence :', sequence

    # break the sequence into words, and break each word into characters
    blocks = [[c.replace('2', '') for c in word.split('3')]
              for word in sequence.split('4')]

    print '[Log] Broke the sequence into words :', blocks

    # decode each character
    message = ' '.join(''.join(guess_char(c) for c in word)
                       for word in blocks)

    print '[Log] Decoded message :', message

    return message

def test():
    ''' Test function '''
    s = [8, 0, 2, 5, 6, 10, 20, 1, 2, 5, 11, 30, 25]
    print 'Samples :', s
    print 'Separating the samples into 3 groups...'
    seps = separate_samples(s, 3)
    print 'Boundary between the groups (separators) :', seps
    groups = [[e for e in s if e < seps[0]],
              [e for e in s if seps[0] <= e < seps[1]],
              [e for e in s if e >= seps[1]]]
    print 'Groups :', groups

    print '------------------------------'

    s = [(1, 3), (4, 6), (7, 10), (14, 20), (21, 27), (30, 35), (50, 52)]
    print 'Signals :', s
    message = decode_signals(s)
    print 'Decoded :', message

if __name__ == '__main__':
    test()
