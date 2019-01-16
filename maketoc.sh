#!/bin/bash

titles=$(grep -A 4 '"cell_type": "markdown"' $1 | grep '"#')
python -c "titles = '''${titles}'''
for line in titles.splitlines() :
    line = line.replace('\"', '')
    splitline = line.split()
    n = len(splitline[0])-1
    print(' ' * max(4 * (n-1) - 1, 0), '-', '[{0}](#{1})'.format(' '.join(splitline[1:]), '-'.join(splitline[1:])))
"
