#!/bin/bash

git checkout master
git pull origin master
git checkout gh-pages
git merge -m "Merge master" master
(make > stdout-make 2> stderr-make \
	&& git commit -a -m "Build." \
	&& git push origin gh-pages) || \
    (echo 'make failed, stderr:' && cat stderr-make)
git checkout master
