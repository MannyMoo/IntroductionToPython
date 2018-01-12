
all : index.html SUPAPYT-IntroductionToPython.html SUPAPYT-LabProblems.html SUPAPYT-LabProblems-Completed.html

SUPAPYT-IntroductionToPython.html : SUPAPYT-IntroductionToPython.ipynb
	@sed -i '' 's/"help()"/"#help()"/' $<
	jupyter-nbconvert --to html --execute --allow-errors $<
	@sed -i '' 's/"#help()"/"help()"/' $<

%.html : %.ipynb
	jupyter-nbconvert --to html --execute --allow-errors $<

