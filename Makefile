
all : index.html SUPAPYT-IntroductionToPython.html SUPAPYT-LabProblems.html
	git commit -a -m "Updating pages"
	git push origin gh-pages 
	git checkout master

%.html : %.ipynb
	git checkout gh-pages
	git pull origin master
	jupyter-nbconvert-2.7 --to html $<

