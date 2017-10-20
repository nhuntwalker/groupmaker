# -*- coding: utf-8 -*-

import os
import json
import random
from collections import defaultdict
import sys


def choose_pairs(student_list, filepath='past_pairs.json'):
    """Choose pairs from a list of students."""
    if os.path.exists(filepath):
        with open(filepath) as f:
            past_pairs = json.load(f)
    else:
        past_pairs = defaultdict(list)
    choices = {}
    for student in student_list:
        choices[student] = set(student_list) - set([student] + past_pairs[student])

    pairs = []
    assigned = set()
    for student in sorted(choices, key=lambda x: len(choices[x])):
        if student not in assigned:
            try:
                pair = random.choice(list(choices[student]))
                pairs.append((student, pair))
                past_pairs[student].append(pair)
                past_pairs[pair].append(student)
            except IndexError:
                index = random.randint(0, len(pairs) - 1)
                past_pairs[student].extend(list(pairs[index]))
                for s in pairs[index]:
                    past_pairs[s].append(student)
                pairs[index] += (student,)
            assigned.update((pair, student))
            for stud in choices:
                for x in (student, pair):
                    if x in choices[stud]:
                        choices[stud].remove(x)

    with open(filepath, 'w') as f:
        json.dump(past_pairs, f)

    return pairs


def main():
    """The main executable function."""
    student_list = open(sys.argv[1]).readlines()
    cached_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cached')
    cached_file = os.path.join(
        cached_dir,
        os.path.splitext(os.path.split(sys.argv[1])[-1])[0] + '.json'
    )
    pairs = choose_pairs(student_list, cached_file)
    output = "Groups:\n"
    for pair in pairs:
        if len(pair) == 2:
            output += "\t{} and {}\n".format(pair[0].strip(), pair[1].strip())
        elif len(pair) == 3:
            output += "\t{}, {}, and {}\n".format(pair[0].strip(), pair[1].strip(), pair[2].strip())
    print(output)

if __name__ == "__main__":
    main()
