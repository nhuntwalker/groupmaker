"""Helpers to the pair creator."""
import os
import json


def clear_cache(path='past_pairs.json'):
    """Remove past pair history."""
    if os.path.exists(path):
        os.remove(path)


def remove_all_traces(name, dictionary, remove_key=False):
    """Remove all traces of name from dictionary with iterable values."""
    if remove_key:
        del dictionary[name]
    for iterable in dictionary.values():
        try:
            iterable.remove(name)
        except:
            pass


def drop_student(name, path='past_pairs.json'):
    """Remove a student from the cache."""
    with open(path) as f:
        past_pairs = json.load(f)
    remove_all_traces(name, past_pairs, remove_key=True)
    with open(path, 'w') as f:
        json.dump(past_pairs, f)


def create_past_pairs(pairs):
    """Create past pairs dict using pairs(list of tuples)."""
    past_pairs = {}
    for pair in pairs:
        for s in pair:
            past_pairs[s] = [x for x in pair if x != s]
    return past_pairs
