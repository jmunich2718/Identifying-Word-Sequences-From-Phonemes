# Identifying-Word-Sequences-From-Phonemes
A pet project to create code that will take a sequence of phonemes and identify possible word combinations it could be and evaluate likely options.

Goal: Given a sequence of phonemes as input (e.g. ["DH", "EH", "R", "DH", "EH", "R"]), find all the combinations of the words that can produce this sequence (e.g. [["THEIR", "THEIR"], ["THEIR", "THERE"], ["THERE", "THEIR"], ["THERE", "THERE"]]). Extension: Find the most likely combinations and reconstruct what was said (e.g. "There, there.").

IDE: Spyder 6 for Windows 10+. 

## Files and Dependencies: 

WordCombos.py : Contains the a function to identify words from phonemes. Doesn't handle edge cases where smaller words could be found first though.

WordCombos2.py : Debugging to try and fix the issue with smaller words.

TesterCode.py : A script to test the function's performance and whether it can handle bad inputs.

My code requires the python wrapper for cmudict, installable with pip:

`pip install cmudict`

See also: https://pypi.org/project/cmudict/

## Resources:

ARPAbet on Wikipedia: https://en.wikipedia.org/wiki/ARPABET

Carnegie Mellon University Pronunciation dictionary: http://www.speech.cs.cmu.edu/cgi-bin/cmudict

## Notes and Unresolved Issues

Full disclosure, I found this exact question with a solution on Kaggle, here: https://www.kaggle.com/code/kamaljitgrewal/find-possible-words-from-phonemes

I have designed and coded my own solution to be my own work, trying not to take anything from that other approach. 

### Initial Attempt: Making WordCombos

The example in the problem does not appear to account for contractions (eg they're). My solution does account for that.

```
Input: ('DH', 'EH1', 'R', 'DH', 'EH2', 'R')
Output: [['their', 'there', "they're"], ['their', 'there', "they're"]]
```

This is good. But upon testing other words, I find problems. This code stops trying after finding a word, any word, even if there could have been other words that were longer. To illustrate this bug, take these examples:


Example 1: "Hello there"

```
Input: ('HH', 'AH1', 'L', 'OW2','DH', 'EH1', 'R')
Output: [['huh'], ['lo', 'loe', 'loew', 'loewe', 'loh', 'low', 'lowe'], ['their', 'there', "they're"]]
```

Note: It stops once it finds the word "huh" instead of going all the way to find the word "hello". It still finds a valid sequence of words, but I wish it to find ALL valid sequences of words instead of stopping here.

Example 2: "bout"

```
Input: ('B', 'AW1', 'T')
Output: [['bao', 'bough', 'bow']]
```

It found a word for the first two phonemes, and then was only left with 'T'. There is no word that is only that one phoneme, so it stopped there and never found "bout".

### Debugging: Making WordCombos2

I could "jolt" it out of this by making it iterate over j, but that gives a LOT of redundant answers and starts to take a long time to compute on my poor old desktop. There has to be a more efficient way. 

I think I have successfully done this with the dummy variable j_old. Initially, the results were not in a clean format though. For example, when given "hello there", it would do the following:

```
Input: ('HH', 'AH1', 'L', 'OW2','DH', 'EH1', 'R')
Output: [['huh'], ['lo', 'loe', 'loew', 'loewe', 'loh', 'low', 'lowe'], ['their', 'there', "they're"], ['hull'], ['au', 'aux', 'eau', 'eaux', 'o', "o'", 'o.', 'oh', 'ohh', 'ow', 'owe'], ['their', 'there', "they're"], ['hello'], ['their', 'there', "they're"]]
```

This is great! It got what I wanted on the final iteration. It's not an ideal format, though, given that it doesn't separate the guesses. 

My final solution for this code is to flatten the answers a bit. See the example output now for "hello there":

```
Input: ('HH', 'AH1', 'L', 'OW2','DH', 'EH1', 'R')
Output: [['huh', 'lo', 'loe', 'loew', 'loewe', 'loh', 'low', 'lowe', 'their', 'there', "they're"],
['hull', 'au', 'aux', 'eau', 'eaux', 'o', "o'", 'o.', 'oh', 'ohh', 'ow', 'owe', 'their', 'there', "they're"],
['hello', 'their', 'there', "they're"]]
```

Good enough for now. Ultimately, I'd like a 3-D matrix, but this is very human-readable at least so I'm going to stop here.

## Future Possibilities

The most obvious area that could be improved is in formatting the output in the cases handled by WordCombos2, where there is the chance of larger words being made up of smaller words. To drill down on this though, it would be most useful to know what the output is being used for. Does it need to be human-readable, or is it being fed into a neural network to see if it can construct the most likely sentence, for example?

Another area that I'm not happy with is the computational power this is requiring. The runtime is high on a home desktop computer; if this were to be designed for a cell phone app or something similar, it would quickly hit up against computational limitations. The first avenue I'd explore to lower computational load would be to further  pre-process the CMU dictionary dataframes. Intuitively, it would speed things up quite a bit if the dictionary was sorted by the first phoneme in each pronunciation, and then split up into a separate dataframe for each phoneme. This would result in 39 smaller dictionary segments, and searching could be limited to the one with the correct starting phoneme.

I could also store the 39 dictionaries as output files from one program, and read them in the main program, rather than have the program process the full dictionary every time it starts. This might help, though I suspect that the biggest computational cost is the searching rather than the pre-processing.

It's easy to imagine that the reduction in computational power from this alone would make it more feasible for fast completion times on a variety of devices of traditionally lower computing power.

I'm sure there are areas for further efficiency improvements. If we stop looking for EVERY possible word combination and only want the n most common ones, for example, we could incorporate some linguistics or statistical knowledge to speed things up. For example, some words are very common and others are incredibly rare; there may be room to sort the dictionaries by frequency of general use rather than alphabetically. 

Moving more towards a machine-learning-like program, one could also start introducing probability of the next word being X given that you found Y. For example, a RNN could allow the program to account for having found one word and then predict what words are more likely to come after that word and search those first.  Allowing backpropagation might have some fun effects as well.

## CMU Dictionary License 

Copyright (c) 2015, Carnegie Mellon University
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of dictTools nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
