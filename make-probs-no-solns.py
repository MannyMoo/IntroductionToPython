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

newcells = []
lastadd = ''
for cell in jprobs['cells'] :
    if cell['cell_type'] == 'code':
        if lastadd != 'code':
            newcells.append(codecell)
            lastadd = 'code'
    else:
        newcells.append(cell)
        lastadd = 'notcode'
jprobs['cells'] = newcells

with open('SUPAPYT-LabProblems.ipynb', 'w') as fprobs :
    json.dump(jprobs, fprobs)
