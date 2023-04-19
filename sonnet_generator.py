# -*- coding: utf-8 -*-
"""
# Markov-Chain Text Generators

Markov-Chain Text Generators work based on statistics on which word normally follows another word. Similar concepts are used in many large language models such as GPT3, ChatGPT, and autocomplete / auto-suggestion on smartphone keyboard apps.

An open-source implementation can be found here:
[https://github.com/jsvine/markovify](https://github.com/jsvine/markovify)

# Load a text corpus

A text corpus is a large set of texts that is used to train a language model.

For now, we will use the text of all Shakespeare's sonnets as our text corpus.
"""

# Download the TXT file containing the text corpus
!wget https://raw.githubusercontent.com/brunoklein99/deep-learning-notes/master/shakespeare.txt

# Read the TXT file and store it in a Python string
filename = 'shakespeare.txt'
corpus = open(filename, 'r').read()
print('Loaded %d bytes from %s' % (len(corpus), filename))

"""# Pre-processing and cleaning"""

# Since certain punctuation marks have special meaning,  
# we need to split them when they are attached to words.
# This can be done by adding a space.
corpus = corpus.replace(',', ' ,')
corpus = corpus.replace('.', ' .')

# Replace certain punctuation as commas and others as periods
corpus = corpus.replace(':', ' ,')
corpus = corpus.replace(';', ' ,')
corpus = corpus.replace('?', ' .')
corpus = corpus.replace('!', ' .')

# Remove unwanted punctuation
corpus = corpus.replace('(', '')
corpus = corpus.replace(')', '')

# Now we can use the split() function to split the string
# into a list of individual words
words = corpus.split()
print('Found %d words' % len(words))

# Convert all words into lowercase characters
words = [w.lower() for w in words]

# Print out the first 20 words
print(words[:20])

"""# Build the Markov Chain

Builds the Markov model by representing it as a Python dictionary. Returns a dict of dicts where the keys of the outer dict represent all possible states,
and point to the inner dicts. The inner dicts represent all possibilities
for the "next" item in the chain, along with the count of times it appears in the text corpus.

Beginning and end of sentences are indicated by the `'.'` character
"""

# implement a function that builds the markov chain
# iterate through the input list of words and for each index i,
# increment model[words[i]][words[i+1]] by one

def build_markov_chain(words):
    # Markov chain model is represented as a Python dictionary of counts
    model = {}

    def add_to_model(current_word, next_word):
      if current_word not in model:
        model[current_word] = {}
      if next_word not in model[current_word]:
        model[current_word][next_word] = 0
      model[current_word][next_word] += 1

    # remember to map '.' to the first word since it is the
    # beginning of a sentence
    add_to_model('.', words[0])
    for i in range(len(words) - 1):
      add_to_model(words[i], words[i+1])
    return model

model = build_markov_chain(words)
print('Built a Markov chain model with %d words' % len(model))

print(model['quick'])
# should return {'fire': 1, 'change': 1, 'objects': 1}

print(model['many'])
# should return {',': 4, 'maiden': 1, 'a': 4, 'lambs': 1, 'gazers': 1, 'nymphs': 1, 'legions': 1}

# shows the list of possible words that can be used to start a sentence
print(model['.'])

#   implement a function that computes the probability 
#   distribution over all possible next words from a given current word
#   and stores it in a dictionary 'model_probs'
#   For any word in the corpus, model_probs should map it to a tuple containing
#   a list of the next word options and a list of the associated probabilities

def compute_probability_distribution(model):
    model_probs = {}
    for current_word in model:
      sum_of_counts = 0
      for next_word in model[current_word]:
        sum_of_counts += model[current_word][next_word]

      next_word_options = []
      next_word_probabilities = []
      for next_word in model[current_word]:
        next_word_options.append(next_word)
        next_word_probabilities.append( model[current_word][next_word] / sum_of_counts)
      model_probs[current_word] = (next_word_options, next_word_probabilities)

    return model_probs

model_probs = compute_probability_distribution(model)
print('Computed the probability distribution for %d words' % len(model_probs))

print(model_probs['quick'])
# should return (['fire', 'change', 'objects'], [0.3333333333333333, 0.3333333333333333, 0.3333333333333333])

print(model_probs['many'])
# should return ([',', 'maiden', 'a', 'lambs', 'gazers', 'nymphs', 'legions'], [0.3076923076923077, 0.07692307692307693, 0.3076923076923077, 0.07692307692307693, 0.07692307692307693, 0.07692307692307693, 0.07692307692307693])

"""# Generating Text"""

#       implement a function that randomly generates the next word
#       given a Markov chain model and a specified current word
# Hint: use the function numpy.random.choice, which
#       draws a random sample from a discrete distribution
# e.g. np.random.choice(['a', 'b', 'c'], p=[0.2, 0.3, 0.5])
#       returns either 'a', 'b', or 'c' with probability 0.2, 0.3, 0.5 respectively
import numpy as np

def generate_next_word(model_probs, current_word):
  next_word_options, next_word_probabilities = model_probs[current_word]
  return np.random.choice(next_word_options, p = next_word_probabilities)

print(generate_next_word(model_probs, 'quick'))
# should randomly return either fire, change, or objects

#       implement a function that randomly generates a phrase
#       starting with the beginning of sentence symbol ('.')
#       continue generating words until either ',' or '.' is encountered

def generate_phrase(model_probs):
    current_word = '.'
    phrase = ''
    while True:
      next_word = generate_next_word(model_probs, current_word)
      if next_word in [',', '.']:
        return phrase[:-1] + next_word
      else:
        phrase += next_word + ' '
        current_word = next_word
    return phrase

print(generate_phrase(model_probs))
# should return a phrase ending in either ',' or '.'

#       implement a function that randomly generates a sonnet
#       in the style of Shakespeare.
#       A sonnet is a poem with 14 lines.
#       Remember to capitalize the first letter of each sentence
#       and add punctuation in appropriate locations.
#       Filter out phrases that are too long or too short
#       The rhyming scheme may be ignored for this function.

def generate_sonnet(model_probs):
    sonnet = ''
    for i in range(14):
      while True:
        phrase = generate_phrase(model_probs)
        if len(phrase) > 30 and len(phrase) < 50:
          break
      sonnet += phrase[0].upper() + phrase[1:] + '\n'
    return sonnet

print(generate_sonnet(model_probs))

"""# Using a different corpus

Let's try using a dataset of user reviews of electronic items on Amazon.com
as our text corpus
"""

!wget -O amazon.json "https://datasets-server.huggingface.co/first-rows?dataset=amazon_us_reviews&config=Electronics_v1_00&split=train"

# Use the JSON library to parse the text data
import json
filename = 'amazon.json'
data = json.load(open(filename, 'r'))
print('Found %d lines of data in %s' % (len(data['rows']), filename))

# Pre-processing and cleaning
corpus = ''
for row in data['rows']:
    line = row['row']['review_body']
    if not line[-1] == '.':
        line += '.'
    corpus += line + ' '

corpus = corpus.replace(',', ' ,')
corpus = corpus.replace('.', ' .')
corpus = corpus.replace('<br />', '')
corpus = corpus.replace('(', '')
corpus = corpus.replace(')', '')

words = corpus.split()
words = [w.lower() for w in words]
print('Found %d words' % len(words))
print(words[:20])