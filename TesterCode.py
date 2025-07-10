# -*- coding: utf-8 -*-
"""
Created on Tue Jun 24 11:50:52 2025

@author: jmunich
"""

# Testing the code.

import WordCombos2 as wc


# Can I find all the variations of a single word?    
test_phonemes1 = ('DH', 'EH1', 'R')
test_phonemes2 = ('B', 'AW1', 'T') # this should be the first entry in the
                                   # dictionary, and return 'bout (at least)


# Can I find combinations of possible words? Note: this is the final objective.
test_phonemes3 = ('DH', 'EH1', 'R', 'DH', 'EH2', 'R')

# How about combinations of words that aren't the same?
# This should be "hello there" 
test_phonemes4 = ('HH', 'AH1', 'L', 'OW2','DH', 'EH1', 'R')

# Does my code handle the wrong type or structure of input?
test_phonemes5 = 5.2

# Does my code handle sequences that are too long?
test_phonemes6 = ('DH', 'EH1', 'R', 'DH', 'EH2', 'R',
                  'DH', 'EH1', 'R', 'DH', 'EH2', 'R',
                  'DH', 'EH1', 'R', 'DH', 'EH2', 'R',
                  'DH', 'EH1', 'R', 'DH', 'EH2', 'R',
                  'DH', 'EH1', 'R', 'DH', 'EH2', 'R',
                  'DH', 'EH1', 'R', 'DH', 'EH2', 'R',
                  'DH', 'EH1', 'R', 'DH', 'EH2', 'R',
                  'DH', 'EH1', 'R', 'DH', 'EH2', 'R',
                  'DH', 'EH1', 'R', 'DH', 'EH2', 'R',
                  'DH', 'EH1', 'R', 'DH', 'EH2', 'R',
                  'DH', 'EH1', 'R', 'DH', 'EH2', 'R')
                  


Words = wc.find_word_combos_with_pronunciation(test_phonemes4)
print('Final results:')
print(Words)
