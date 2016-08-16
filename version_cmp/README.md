# version_cmp


get the means and standard deviations for all results:

        usage:python version_cmp.py -o /tmp/asdf -s  /tmp/sample200/

plot all results:

        usage:python version_cmp.py -o /tmp/asdf -a  /tmp/sample200/

plot all versions on one datasets results unsorted:

        usage:python version_cmp.py -o /tmp/asdf -d 200 /tmp/sample200/
        
plot all versions on one datasets results sorted:

        usage:python version_cmp.py -o /tmp/asdf -d 200 --order ~/data_order /tmp/sample200/

plot some versions on one dataset:

        usage:python version_cmp.py -o /tmp/asdf -d 200 -t 6460565be... -t 9b9d6d8...  /tmp/sample200/

report automatically if there is a pair of versions whose p-value is smaller 5% in t-test:

        usage:python version_cmp.py -o /tmp/asdf -d 200 -r /tmp/sample200/