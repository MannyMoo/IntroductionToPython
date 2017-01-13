
all : index.html SUPAPYT-IntroductionToPython.html SUPAPYT-LabProblems.html

%.html : %.ipynb
	ipython nbconvert --to html $<
