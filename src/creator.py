# -*- coding: utf-8 -*-

import os
import sys
import json
import argparse
from collections import defaultdict
from helpers import remove_all_traces, create_past_pairs, remove_from_cache


def get_past_pairs(cachepath):
    """Retrieve cache if it exists, otherwise return empty dict of lists."""
    if os.path.exists(cachepath):
        with open(cachepath) as f:
            past_pairs = json.load(f)
    else:
        past_pairs = defaultdict(list)
    return past_pairs


def choose_pairs(student_list, past_pairs):
    """
    Choose pairs from a list of students.

    Returns:
        pairs(list of tuples), past_pairs(dict with values of lists)
    """
    choices = {}
    for student in student_list:
        choices[student] = (set(student_list) -
                            set([student] + past_pairs[student]))
    if any(len(chcs) == 0 for chcs in choices.values()):
        raise Exception('A student has been paired with everyone.')
    pairs = []
    assigned = set()
    for student in sorted(choices, key=lambda x: len(choices[x])):
        if student not in assigned:
            try:
                partner = max(choices[student], key=lambda s: len(past_pairs[s]))
                new = (student, partner)
                pairs.append(new)
                past_pairs[student].append(partner)
                past_pairs[partner].append(student)
            except ValueError:
                cands = defaultdict(list)
                for p in pairs:
                    cands[len(set(p) & set(past_pairs[student]))].append(p)
                best_pairs = cands[min(cands)]
                best_pair = min(
                    best_pairs or pairs,
                    key=lambda p: max(len(past_pairs[s]) for s in p))
                past_pairs[student].extend(list(best_pair))
                for s in best_pair:
                    past_pairs[s].append(student)
                pairs[pairs.index(best_pair)] += (student,)
                new = (student,)
            assigned.update(new)
            for x in new:
                remove_all_traces(x, choices)
    return pairs, past_pairs


def write_past_pairs(past_pairs, cachepath):
    """Write the past_pairs to json."""
    with open(cachepath, 'w') as f:
        json.dump(past_pairs, f)


def drop_student():
    """Command line function to remove a dropped student."""
    parser = argparse.ArgumentParser()
    parser.add_argument('name', type=str)
    parser.add_argument('cachepath', type=str)
    args = parser.parse_args()
    remove_from_cache(args.name, args.cachepath)


def main():
    """The main executable function."""
    parser = argparse.ArgumentParser()
    parser.add_argument('list_file', type=str, help='.txt file listing individuals')
    parser.add_argument('-n', '--no-cache',
                        help='create pairs ignoring cache',
                        action='store_true')
    parser.add_argument('-r', '--reset-cache',
                        help='reset cache to data created by current run',
                        action='store_true')
    args = parser.parse_args()

    student_list = [line.rstrip() for line in open(args.list_file)]
    cached_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cached')
    cached_file = os.path.join(
        cached_dir,
        os.path.splitext(os.path.split(args.list_file)[-1])[0] + '.json'
    )
    if args.no_cache:
        past_pairs = defaultdict(list)
    else:
        past_pairs = get_past_pairs(cached_file)
    pairs, past_pairs = choose_pairs(student_list, past_pairs)
    if args.reset_cache:
        past_pairs = create_past_pairs(pairs)
    if not args.no_cache or (args.reset_cache and args.no_cache):
        write_past_pairs(past_pairs, cached_file)

    output = "Groups:\n"
    for pair in pairs:
        if len(pair) == 2:
            output += "\t{} and {}\n".format(*pair)
        elif len(pair) == 3:
            output += "\t{}, {}, and {}\n".format(*pair)
    print(output)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main()
