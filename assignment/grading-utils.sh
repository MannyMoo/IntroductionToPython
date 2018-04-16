#!/bin/bash

function grades-to-pdf() {
    if [ ! -z "$1" ] ; then
	fname=$1
    else
	fname=MarkingCriteria.ods
    fi
    soffice --convert-to pdf $fname
}

function next-student() {
    nextstudent=$(python -c "import os
dirs = sorted(os.listdir('..'))
pwd = os.getcwd().split(os.sep)[-1]
ipwd = dirs.index(pwd)
if ipwd == len(dirs) - 1 :
    print 'You\\'re done!'
else :
    print dirs[ipwd+1]
")
    if [ "$nextstudent" = "You're done!" ] ; then
	echo $nextstudent
    else
	cd ../$nextstudent
	open *.ods
    fi
}
