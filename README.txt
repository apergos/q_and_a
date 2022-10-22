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
  you can use the default QandA.templ if you like
* create some intro html text that will go after the body tag and
  before the topics in the output; the Intro.html is what I use with
  the topics in the topics directory currently
* run q_and_a.py -t path-to-template -i path-to-intro -d path-to-topicsdir > new-html-file.html
* check that you like the results
* profit

Subject to change at my slightest whim.

This really should not hardcode in things like the body bgcolor tag, and the start/end
topic html. Yuck.







