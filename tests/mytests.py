from handyfuncs import (
    merge_dictionaries
    , number_of_words_in_string
    , get_initials
    )

d1 = {
      'clothes': ['shoes', 'socks', 'ties']
      , 'food': ['cheese', 'bananas', 'lentils']
      }
d2 = {
      'clothes': ['shoes', 'socks', 'shorts', 'hats']
      , 'cutlery': ['knives', 'forks']
      }
d3 = merge_dictionaries(d1, d2)

number_of_words_in_string("what is going on")

get_initials("help me please")