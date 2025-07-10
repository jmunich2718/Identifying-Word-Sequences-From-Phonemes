# -*- coding: utf-8 -*-
"""
Created on Tue Jun 24 11:50:00 2025

@author: jmunich
"""

import pandas as pd
import cmudict

###############################
# Prep the dictionary for use #
###############################

cmudictionary = cmudict.entries()
dict_df = pd.DataFrame(cmudictionary, columns = ['Word', 'Phonemes'])

# Clean this dictionary of numbers, since our input will not have any.
# If our input does have any, it, too, will be cleaned.
dict_phonemes = dict_df['Phonemes']
dict_words = dict_df['Word']
dict_phonemes_clean = []

for i in range(len(dict_phonemes)):
     clean_phoneme = []
     for character in dict_phonemes[i]:
         if character.isalpha(): clean_phoneme.append(character)
         else: clean_phoneme.append(character[:-1])
     dict_phonemes_clean.append(clean_phoneme)
     
dict_clean = {'Word': dict_words, 'Phonemes': dict_phonemes_clean}
dict_df_clean = pd.DataFrame(dict_clean)


# Make a list of possible phonemes to validate input against. Reference CMU
# website.
AcceptedPhonemes = ['AA', 'AE', 'AH', 'AO', 'AW', 'AY',
                    'B', 'CH', 'D', 'DH',
                    'EH', 'ER', 'EY',
                    'F', 'G', 'HH',
                    'IH', 'IY', 
                    'JH', 'K', 'L', 'M', 'N', 'NG',
                    'OW', 'OY',
                    'P', 'R', 'S', 'SH', 'T', 'TH',
                    'UH', 'UW',
                    'V', 'W', 'Y', 'Z', 'ZH']


########################
# Function definitions #    
########################                  
    
def input_cleaning(phonemes):    
    '''
    Sub-routine. Validates and cleans input.
    
    Args: 
        phonemes: the input
    Returns:
        phonemes_clean: cleaned up data, validated and ready to process
    '''
    
    if not isinstance(phonemes, (list, tuple)): 
        raise TypeError('phonemes must be a sequence.')

    for element in phonemes:
        if not isinstance(element, str):
            raise TypeError('Each element in phonemes must be a string.')
      
    
    # Make sure the input isn't going to overwhelm my computer. Upon some
    # minimal research, the longest reasonable words in the English language
    # appear to be about 20 phonemes. Let's put the limit at 50 for now.
    if len(phonemes) > 50.: raise TypeError('Please keep the length under 50 '
                                            'phonemes')
    
    # scrub phonemes of numbers and make sure they are recognized phonemes
    phonemes_clean = []
   
    for i in range(len(phonemes)):
         clean_phoneme = ''
         for character in phonemes[i]:
             if character.isalpha(): clean_phoneme += character
         
         
         if clean_phoneme in AcceptedPhonemes:
             phonemes_clean.append(clean_phoneme)
         else: raise ValueError('Each element in phonemes must correspond to a'
                              ' recognized phoneme in ARPAbet representation.')

    print('inputs validated: ', phonemes_clean)
    return phonemes_clean


def make_phoneme_chunk(phonemes_clean,i,j):
    '''
    Sub-routine. Creates a sequence of phonemes for the requested chunk. 
    
    Args: 
        phonemes_clean: the input sequence of phonemens
        i: the position of the first desired phoneme of the chunk
        j: the position of the last desired phoneme of the chunk
    Returns:
        phoneme_chunk: The desired sub-sequence of the original phoneme sequence.
    '''
    
    phoneme_chunk = phonemes_clean[i:j+1]
    return phoneme_chunk


def find_words(phonemes):
    '''
    Sub-routine.
    
    Matches one specific set of phonemes to words.

    Args:
        phonemes : the series of phonemes to match to words

    Returns:
        words: pandas database of matching words
    '''
    mask = dict_df_clean['Phonemes'].isin([phonemes])
    words = dict_df_clean[mask]
    return words
            

def find_next_word(phonemes_clean,i,j,words_so_far, done_flag, j_placeholder):
     '''
    Searches for all possible words that match the phoneme sequence. Print statements were used for debugging.
    
    Args: 
        phonemes_clean: the input sequence of phonemens
        i: lower limit for the search
        j: upper limit for the search
        words_so_far: an array of the word sequences found so far, before starting this function.
    Returns:
        words_so_far: an array of possible word sequences that includes the input words_so_far, and adds further results to the end.
    '''
    
    j_old=0

    while done_flag == False:

        phoneme_chunk = make_phoneme_chunk(phonemes_clean, i, j)
        #print('(i,j) = (', i, ',', j, ') ; phoneme chunk:', phoneme_chunk) 
        words = find_words(phoneme_chunk)
        if j_placeholder != 0:
            #print('This is a second round. First words match: ')
            #print(words)
        
        while words.empty and j<len(phonemes_clean): 
#            print('No word matches. Incrementing j by 1.') 
            #add a phoneme and try again
            j += 1
            phoneme_chunk = make_phoneme_chunk(phonemes_clean, i, j)
            #print('(i,j) = (', i, ',', j, ') ; phoneme chunk:', phoneme_chunk) 
            words = find_words(phoneme_chunk)
        if not words.empty:
            words_list = words['Word'].tolist()
            words_so_far.append(words_list)
            if j_old <= j_placeholder:
                j_old = j+1
               
        #print(words_so_far)

        #print('Match found, now looking for a subsequent word with remaining ',
              'phonemes.')

        i = j+1
        j = i
        
        if j+1 >= len(phonemes_clean): 
            done_flag = True
            print('Done')
            return words_so_far, j_old
            

    words_so_far = find_next_word(phonemes_clean, i, j, words_so_far, done_flag, j_old)
        
#        print('I am done this pass.')
    #return words_so_far


def find_word_combos_with_pronunciation(phonemes):
    '''
    Given phonemes, a sequence of strings each representing one English
    phoneme, returns all possible combinations of words represented by that 
    sequence of phonemes.
    
    Assumptions and limitations: 
        
        This code uses the Carnegie Mellon University's (CMU) pronounciation
        dictionary, version cmudict-0.7b [First released November 19, 2014]. 
        This uses the ARPAbet phoneme set. See README for licensing. 
        
        I have not tried to account for regional variations on pronounciations,
        slurring of words, or other variations beyond what exists in the CMU 
        dictionary. Variations in the 7.0b version of CMU's dictionary are 
        included.
        
        I have not accounted for stresses (represented as numbers in the CMU
        dictionary).
        
        I have limited the number of input phonemes to 50 for the moment, to
        avoid possible overwhelm if someone tries to input an entire novel or
        something similar.
    
    Args:
        phonemes (sequence of strings representing English phonemes): an
        ordered sequence of phonemes representing something said.
        
    Returns: array of possible word combinations that the input might have been
    '''
    
    phonemes_clean = input_cleaning(phonemes)
    words_so_far = list()
    
    Initial_Result, j_old = find_next_word(phonemes_clean, 0, 0, words_so_far, False, 0)
    Cleaned_Initial_Result = [x for x in Initial_Result if x != []]
    Formatted_Initial_Results = []
    for row in Cleaned_Initial_Result:
        Formatted_Initial_Results.extend(row)

    Final_Results = []
    Final_Results.append(Formatted_Initial_Results)

    print('j_old = ', j_old)
    

    while 0 < j_old < len(phonemes_clean):
        words_so_far = list() 
        Extra_Result, j_old = find_next_word(phonemes_clean, 0, j_old, words_so_far, False,j_old)
        Cleaned_Extra_Result = [y for y in Extra_Result if y != []]
        Formatted_Extra_Result = []
        for row in Cleaned_Extra_Result:
            Formatted_Extra_Result.extend(row)

        Final_Results.append(Formatted_Extra_Result)


    Cleaned_Final_Results = [z for z in Final_Results if z != []]    
    return Cleaned_Final_Results

    









