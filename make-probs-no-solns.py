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
lasttype = ''
lastadd = ''
for cell in jprobs['cells'] :
    if cell['cell_type'] != 'code' and lasttype == 'code' and lastadd != 'code' :
        newcells.append(codecell)
    lasttype = cell['cell_type']
    if cell['cell_type'] != 'code' or (cell['source'] and cell['source'][0].startswith('#_')) :
        newcells.append(cell)
        lastadd = cell['cell_type']
        
jprobs['cells'] = newcells

with open('SUPAPYT-LabProblems.ipynb', 'w') as fprobs :
    json.dump(jprobs, fprobs)
