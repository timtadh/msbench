# html_analyzer

running all datasets through all versions:

        usage:python html_analyzer.py -l 100 -v ~/research/examples/html-versions -r 5 -o /tmp/test/ ~/research/samples

running one dataset through all versions

		usage:python html_analyzer.py -l 100 -v ~/research/examples/html-versions -d -r 5 -o /tmp/test/ ~/research/samples

running all datasets through some versions:

        usage:python html_analyzer.py -l 100 -p ~/research/examples/html-versions/... -p ~/research/examples/html-versions/... -r 30 -o /tmp/test/ ~/research/samples/

running one dataset through some versions:

        usage:python html_analyzer.py -l 100 -p ~/research/examples/html-versions/... -p ~/research/examples/html-versions/... -d -r 30 -o /tmp/test/ ~/research/samples/xxx.html
