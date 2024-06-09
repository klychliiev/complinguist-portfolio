from nltk.corpus import wordnet as wn
from itertools import combinations

# function to filter for similar words (those with path_similarity over 0.1)
def cross_extra_word(*words):
    
    # retrieval of the first definition of each word
    my_words = [wn.synsets(word)[0] for word in words]

    # generation of the 2-word combinations for the input words for their further semantic comparison
    word_combinations = combinations(my_words, 2)    

    # collecting the word pairs having the similarity over 0.1
    similar_words = [[i[0], i[1]] for i in word_combinations if i[0].path_similarity(i[1]) > 0.1]    
    #--> [[Synset('fork.n.01'), Synset('cup.n.01')], [Synset('fork.n.01'), Synset('spoon.n.01')], [Synset('cup.n.01'), Synset('spoon.n.01')]]

    # extraction of semantically similar words
    similar_words = set([element for innerList in similar_words for element in innerList])    
    #--> {Synset('fork.n.01'), Synset('spoon.n.01'), Synset('cup.n.01')}

    print(similar_words)   

# the output returns synsets of semantically similar words. extra words are specified in the comment after each function call
cross_extra_word('love', 'hate', 'cat', 'flag', 'puzzle')    # cat, flag, puzzle
cross_extra_word('fork', 'cup', 'spoon', 'beer')    # beer
cross_extra_word('dog', 'cat', 'flame')    # flame
cross_extra_word('pasta', 'pizza', 'lasagna', 'italian')    # italian
cross_extra_word('tomato', 'onion', 'banana', 'lemon')    # banana