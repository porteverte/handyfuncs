def number_of_words_in_string(my_string):
    
    # make sure we are dealing with a string (in case a float is passed)
    my_string = str(my_string)
    
    # determine the number of words in the string by splitting it into into a list and getting its length    
    return len(my_string.strip().split())

def all_same_character(s, **kwargs):
    
    for k, v in kwargs.items():
        if k == 'c':
            c = v
    
    n = len(s)
    for i in range(1, n):
        if s[i] != c:
            return False
        if s[i] != s[0]:
            return False
 
    return True

def get_initials(s):
    # try:
    return ''.join([x[0] for x in str(s).split()])
    # except AttributeError:
    #     return s

def literal_return(val):
    
    from ast import literal_eval
    
    try:
        return literal_eval(val)
    except (ValueError, SyntaxError) as e:
        return val

def explode_frame_list_column(my_frame, my_column):
        
    # remove blank values -- and make a copy to keep the original frame in tact
    my_frame = my_frame[my_frame[my_column].str.len() > 0].copy()
    
    # evaluate the column -- because the lists are stored as text
    my_frame[my_column] = my_frame[my_column].apply(lambda x: literal_return(str(x)))
    
    # now do the actual explosion
    my_frame = my_frame.explode(my_column)
    
    return my_frame

def convert_dict_to_list(my_dict):
# turns the company suffixes dicitonary into a list to be used in company standardisation    
    my_list = []
    for md in my_dict:
        for my_item in my_dict[md]:
            my_list.append((my_item, md))
    # sort the list by the descending length of the first tuple value
    # this is so that replacments are made to the longest strings first in case one shorter term is inside another longer one 
    # e.g. kg is also at the end of gmbh & co kg so if it found a variant of kg first it would not replace all of the term
    my_list.sort(key=lambda x: len(x[0]), reverse=True)
    return my_list

def merge_dictionaries(d1, d2):
    
    # make copies of dictionaries to avoid messing them up
    d1_copy = d1.copy()
    d2_copy = d2.copy()
    
    # create a list comprising all keys from both dictionaries (convert list to set then back to list to dedupe it)
    my_keys = list(set([*d1_copy] + [*d2_copy]))
    
    # if a key is missing from one of the dictionaries then add it (then both will have exactly the same keys)
    for m in my_keys:
        if not m in d1_copy:
            d1_copy.update({m: None})
        if not m in d2_copy:
            d2_copy.update({m: None})
    
    # create blank dictionary
    d = {}
    
    # add each item in the keys list to the dictionary as a key with None as the value 
    for i in my_keys:
        d[i] = None
    
    # merge the values for the keys in each dictionary and add them to the new one
    for k in d.keys():
        # merge the lists of values (will produce a list of lists)
        merged_lists = [d1_copy[k],d2_copy[k]]
        # remove NoneType from lists
        clean_list = [x for x in merged_lists if x is not None]
        # flatten the list of lists into one plain list
        flat_list = [x for xs in clean_list for x in xs]
        # dedupe the list
        deduped_list = list(set(flat_list))
        # add the list to the dictionary
        d[k] = deduped_list
    
    return d