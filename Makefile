# Currently, html in markdown cells gets rendered as text when converting
# notebooks to html. So they're converted back to proper html after with sed.

all : index.html SUPAPYT-IntroductionToPython.html SUPAPYT-LabProblems.html SUPAPYT-LabProblems-HalfCompleted.html SUPAPYT-LabProblems-Completed.html SUPAPYT-Installation-Instructions.html Getting-started.html

SUPAPYT-IntroductionToPython.html : SUPAPYT-IntroductionToPython.ipynb
	@sed -i '' 's/"help()"/"#help()"/' $<
	jupyter nbconvert --to html --execute --allow-errors $<
	@sed -i '' 's/#help()/help()/' $@
	@sed -i '' 's@<p>&lt;\(img.*\)&gt;</p>@<\1>@' $@
	@sed -i '' 's/"#help()"/"help()"/' $<

%.html : %.ipynb
	jupyter nbconvert --to html --execute --allow-errors $<
	@sed -i '' 's@<p>&lt;\(img.*\)&gt;</p>@<\1>@' $@
