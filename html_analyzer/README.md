# html_analyzer

        usage:
all versions test all samples:
        python html_analyzer.py -l 100 -v ~/research/examples/html-versions -r 5 -o /tmp/test/ ~/research/samples

some versions test all samples:
        python html_analyzer.py -l 100 -p ~/research/examples/html-versions/... -p ~/research/examples/html-versions/... -r 30 -o /tmp/test/ ~/research/samples/

some versions test one sample:
        python html_analyzer.py -l 100 -p ~/research/examples/html-versions/... -p ~/research/examples/html-versions/... -i -r 30 -o /tmp/test/ ~/research/samples/xxx.html
