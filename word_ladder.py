# -*- coding: utf-8 -*-
"""
A word ladder problem is this: given a start word and a goal word, find the shortest way to transform the start word into the goal word by changing one letter at a time, such that each change results in a word. For example starting with `green` we can reach `grass` in 7 steps:

`green` → `greed` → `treed` → `trees` → `tress` → `cress` → `crass` → `grass`

The word ladder game can be played online here:
[https://wordwormdormdork.com/](https://wordwormdormdork.com/)

# Load a dictionary of words
"""

# Download the TXT file containing a list of all valid words
!wget https://raw.githubusercontent.com/aimacode/aima-data/f6cbea61ad0c21c6b7be826d17af5a8d3a7c2c86/EN-text/wordlist.txt

# Read the list of valid words from the TXT file and store it in a Python set data structure
WORDS = set(open('wordlist.txt').read().split())
print('Loaded %d words' % len(WORDS))

"""# Build a graph of neighboring words"""

# implement a function that returns a list of all words that are a one-letter change away from a given word
def get_neighboring_words(word):
    "All words that are one letter away from this word."
    # for each letter position in word and for each letter in the alphabet,
    # attempt to create a new word by replacing one letter
    # add the new word to the list of neighbors if it exists in the list of valid words
    neighbors = [word[:i] + c + word[i+1:]
                 for i in range(len(word))
                 for c in 'abcdefghijklmnopqrstuvwxyz'
                 if c != word[i]]
    neighbors = [n for n in neighbors if n in WORDS]
    return neighbors

get_neighboring_words('hello')
# should return ['cello', 'hallo', 'hillo', 'hollo', 'hullo', 'helio', 'hells']

get_neighboring_words('green')
# should return ['preen', 'treen', 'greed', 'greek', 'grees', 'greet']

"""# State-space Search"""

# Implement the Breadth-first search algorithm
def breadth_first_search(start, goal):
    "Find a shortest sequence of states from start to the goal."
    frontier = [start] # A queue
    previous = {start: None}  # start has no previous state; other states will
    while frontier:
        s = frontier.pop(0)
        if s == goal:
            return path(previous, s)
        for s2 in get_neighboring_words(s):
            if s2 not in previous:
                frontier.append(s2)
                previous[s2] = s
    return "No solution"
                
def path(previous, s): 
    "Return a list of states that lead to state s, according to the previous dict."
    return [] if (s is None) else path(previous, previous[s]) + [s]

breadth_first_search('green', 'grass')
# should return ['green', 'grees', 'greys', 'grays', 'grass']

breadth_first_search('smart', 'brain')
# should return ['smart','scart','scant','slant','plant','plait','plain','blain','brain']

breadth_first_search('frown', 'smile')
# should return ['frown', 'crown', 'crows', 'chows', 'shows', 'shots', 'shote', 'smote', 'smite', 'smile']

# Implement the Depth-first search algorithm
def depth_first_search(start, goal):
    frontier = [start] # A queue of states
    previous = {start: None}  # start has no previous state; other states will
    while frontier:
        s = frontier.pop()
        if s == goal:
            return path(previous, s)
        for s2 in get_neighboring_words(s):
            if s2 not in previous:
                frontier.append(s2)
                previous[s2] = s
    return "No solution"

def path(previous, s): 
    "Return a list of states that lead to state s, according to the previous dict."
    return [] if (s is None) else path(previous, previous[s]) + [s]

depth_first_search('green', 'grass')

"""# Extensions

Implement a Breadth-First Search variant that returns all optimal solutions
"""

# Breadth-First Search for multiple solutions
#   Inputs are the start state and the goal state
#   Returns all optimal paths from start to goal as a list of lists

def bfs_multiple(start, goal):
    "Find multiple sequences of shortest paths from start to the goal."
    frontier = [start] # A queue
    parents = {start: None}  # start has no parent state; other states will
    dist = {start: 0} # distance to the start state is zero

    # main loop of the search algorithm
    while frontier:
        s = frontier.pop(0)

        # check for the goal condition
        if s == goal:
            paths = []
            def find_path(current_state, current_path):
                if current_state == start:
                    paths.append(current_path + [current_state])
                    paths[-1].reverse()
                else:
                    for p in parents[current_state]:
                        find_path(p, current_path + [current_state])
            find_path(goal, [])
            return paths

        # explore neighbors
        for s2 in get_neighboring_words(s):
            if not s2 in parents:
                parents[s2] = []
            if not s2 in dist:
                dist[s2] = dist[s] + 1
                parents[s2].append(s)
                frontier.append(s2)
            elif dist[s2] == dist[s] + 1:
                parents[s2].append(s)

    # if no valid path found, return "No solution"
    return "No solution"

bfs_multiple('cat', 'dog')
# should return [['cat', 'cot', 'dot', 'dog'], ['cat', 'cot', 'cog', 'dog']]

bfs_multiple('cold', 'warm')
# should return [['cold', 'wold', 'word', 'ward', 'warm'],
#                 ['cold', 'cord', 'word', 'ward', 'warm'],
#                 ['cold', 'cord', 'card', 'ward', 'warm'],
#                 ['cold', 'wold', 'word', 'worm', 'warm'],
#                 ['cold', 'cord', 'word', 'worm', 'warm'],
#                 ['cold', 'cord', 'corm', 'worm', 'warm']]