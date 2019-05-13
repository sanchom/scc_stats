#!/usr/bin/python3

import sys

assert len(sys.argv) == 2, 'Must provide a single argument: the input path.'

input_path = sys.argv[1]

f = open(input_path, 'r')
data = f.read()

groups = []

this_group = []
for line in data.splitlines():
    if len(line) == 0:
        if (this_group):
            groups.append(this_group)
        this_group = []
    else:
        this_group.append(line)

groups = sorted(groups, key=lambda group: group[0])

done = False
while (not done):
    changes = False
    for a, group in enumerate(groups[:-1]):
        for b, other_group in enumerate(groups[a+1:], start=a+1):
            # if there is any overlap between elements of group and other group
            overlap = False
            for x in group:
                for y in other_group:
                    if x == y:
                        overlap = True
            if overlap:
                groups[b].extend(group)
                groups[b] = list(set(groups[b]))
                del groups[a]
                changes = True
                break
        if changes:
            break
    if not changes:
        done = True

for g in groups:
    for e in g:
        print(e)
    print()
