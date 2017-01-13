
all : index.html SUPAPYT-IntroductionToPython.html SUPAPYT-LabProblems.html

%.html : %.ipynb
	git checkout gh-pages
	git merge master
	jupyter-nbconvert-2.7 --to html $<

