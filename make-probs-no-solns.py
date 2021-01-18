#!/usr/bin/env python3

import json, shutil

shutil.copy('SUPAPYT-LabProblems-Completed.ipynb', 'SUPAPYT-LabProblems.ipynb')
with open('SUPAPYT-LabProblems.ipynb') as fprobs :
    jprobs = json.load(fprobs)

codecell = {'cell_type': 'code',
            'execution_count': 0,
            'metadata': {},
            'outputs': [],
            'source': []}

# no solutions
newcells = []
# half solutions
halfcells = []
lastadd = ''
n = 0
halfn = 8
for cell in jprobs['cells'] :
    if cell['cell_type'] == 'markdown' and cell['source'][0].startswith('##'):
        n = int(cell['source'][0].strip('#)\n'))
    if cell['cell_type'] == 'code':
        if cell['source'] and cell['source'][0].startswith('# Eg'):
            if n > halfn:
                newcells.append(cell)
            halfcells.append(cell)
            lastadd = 'notcode'
        elif lastadd != 'code':
            if n > halfn:
                halfcells.append(codecell)
            newcells.append(codecell)
            lastadd = 'code'
        if n <= halfn:
            halfcells.append(cell)
    else:
        newcells.append(cell)
        halfcells.append(cell)
        lastadd = 'notcode'

jprobs['cells'] = newcells
with open('SUPAPYT-LabProblems.ipynb', 'w') as fprobs :
    json.dump(jprobs, fprobs)

jprobs['cells'] = halfcells
with open('SUPAPYT-LabProblems-HalfCompleted.ipynb', 'w') as fprobs:
    json.dump(jprobs, fprobs)
