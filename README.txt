What this is, how it works

I wanted a way to collect up a bunch of q&a and related materials on a bunch of topics
and format them nicely in html, expecting that I might move them around a lot, change
order and wording and topic names and all kinda stuff. And doing the html markp by
hand was irritating me so here's this instead.

To use this very basic script, do the following:

* add stuff to the entries in topics/ directory or to a directory
  of yor choosing, number it according to where you want it shown
  in the output
* make an html template for displaying a topic and its entries;
  every sub-entry to be substituted in should use the name of the
  sub-entry in the yaml file, like this: %(name-here)s  and no
  more than one such sub-entry per line in the template file;
  you can use the default html/QandA.templ if you like
* create some intro html text that will go after the body tag and
  before the topics in the output; html/Intro.html is what I use with
  the topics in the topics directory currently
* if you want a fancy html footer, make one, otherwise there is html/Footer.html
* run:
    q_and_a.py -t path-to-template -i path-to-intro -d path-to-topicsdir \
        -f path-to-footer> new-html-file.html
* check that you like the results
* profit

Subject to change at my slightest whim.

This really should not hardcode in the start/end topic html. Yuck.







