
all : index.html SUPAPYT-IntroductionToPython.html SUPAPYT-LabProblems.html SUPAPYT-LabProblems-Completed.html SUPAPYT-Installation-Instructions.html Getting-started.html

SUPAPYT-IntroductionToPython.html : SUPAPYT-IntroductionToPython.ipynb
	@sed -i '' 's/"help()"/"#help()"/' $<
	jupyter-nbconvert --to html --execute --allow-errors $<
	@sed -i '' 's/#help()/help()/' SUPAPYT-IntroductionToPython.html
	@sed -i '' 's/"#help()"/"help()"/' $<

%.html : %.ipynb
	jupyter-nbconvert --to html --execute --allow-errors $<

