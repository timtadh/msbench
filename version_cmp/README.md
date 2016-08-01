# version_cmp

        usage:

get the means and standard deviations for all results:
        python version_cmp.py -o /tmp/asdf -s  /tmp/sample200/

plot all results:
        python version_cmp.py -o /tmp/asdf -a  /tmp/sample200/

plot all versions on one datasets results:
        python version_cmp.py -o /tmp/asdf -d 200 /tmp/sample200/

plot some versions on one dataset:
        python version_cmp.py -o /tmp/asdf -d 200 -t 6460565be... -t 9b9d6d8...  /tmp/sample200/
