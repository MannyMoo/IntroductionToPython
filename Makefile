
all : index.html SUPAPYT-IntroductionToPython.html SUPAPYT-LabProblems.html SUPAPYT-LabProblems-Completed.html

SUPAPYT-IntroductionToPython.html : SUPAPYT-IntroductionToPython.ipynb
	@sed -i '' 's/"help()"/"#help()"/' $<
	jupyter-nbconvert-2.7 --to html --execute --allow-errors $<

%.html : %.ipynb
	jupyter-nbconvert-2.7 --to html --execute --allow-errors $<

