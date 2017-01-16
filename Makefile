
all : index.html SUPAPYT-IntroductionToPython.html SUPAPYT-LabProblems.html

%.html : %.ipynb
	jupyter-nbconvert-2.7 --to html $<

