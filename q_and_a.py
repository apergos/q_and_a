#!/usr/bin/python3
'''
given a little directory with a topic, questions, answers etc
and a formatting template for these, produce one page of html
'''
import os
import sys
import getopt
import yaml


def get_file_contents(path):
    '''return contents of a file at the given path'''
    with open(path, "r") as infile:
        text = infile.read()
        return text


def get_topic_contents(dirpath):
    '''read all files in the specified directory, in numerical
    order, concatenating all the content and returning it'''
    files = os.listdir(dirpath)
    contents = ""
    for topicfile in sorted(files):
        contents += get_file_contents(os.path.join(dirpath, topicfile))
    return contents


def put_html_header():
    '''write a header for an html doc to stdout'''
    print('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" ' +
          '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">')
    print('<html>')
    # FIXME this should not be hardcoded
    print('<body bgcolor="#ffffff">')


def put_html_footer():
    '''write a footer for an html doc to stdout'''
    print('</body>')
    print('</html>')


def put_intro(content):
    '''write the intro text for the q & a doc to stdout'''
    print(content)


def put_topic_start(topic):
    '''write the topic section header with markup to stdout'''
    # FIXME this should not be hardcoded
    print('<details>\n<summary>' + topic + '</summary>\n\n<dl>\n')


def put_topic_end():
    '''write the close topic markup to stdout'''
    # FIXME this should not be hardcoded
    print('</dl>\n</details>\n')


def put_entry(entry, templ):
    '''write out a question with formatting to stdout'''
    print(templ % { "question": entry['question'],
                    "answer": entry['answer'],
                    "readings": entry['readings'],
                    "exercises": entry['exercises']})


def usage(message):
    '''
    display a helpful usage message with an optional
    introductory message first
    '''
    if message is not None:
        sys.stderr.write(message)
        sys.stderr.write("\n")
    usage_message = """
Usage: q_and_a.py [--dir <path>] [--template <path>] [--intro <path>]
                   --help

This script takes a little pile of topics and their questions, answers, reading material
links and excerises, and turns them into one html page for viewing.

Arguments:
  --dir       (-d):  directory where topic files are located
                     default: ./topics
  --tmeplate  (-t):  path to html template into which the text for each question, answer
                     and so on will be inserted
                     default: ./QandA.templ
  --intro     (-i):  path to a file of introductory text, html formtted, which will be
                     prepended to the topic questions
                     default: ./Intro.html
  --help      (-h):  display this help message

Setup:
  Make sure you have your topic files in the format given in the sample.yaml file
  and that the file names are numbered in the order you would like them to appear
  in the html output.

  Any template you create for the output should have placeholders for the topic, question,
  answer, readings and exercises keys for each set of entries.
"""
    sys.stderr.write(usage_message)
    sys.exit(1)


def get_args():
    '''get, validate and return args, overriding defaults as needed'''
    args = {'template': 'QandA.templ', 'intro': 'Intro.html', 'topicsdir': 'topics'}
    try:
        (options, remainder) = getopt.gnu_getopt(
            sys.argv[1:], "d:i:t:h", ["dir=", "intro=", "template=", "help"])
    except getopt.GetoptError as err:
        usage("Unknown option specified: " + str(err))

    for (opt, val) in options:
        if opt in ["-d", "--dir"]:
            args['topicsdir'] = val
        elif opt in ["-i", "--intro"]:
            args['intro'] = val
        elif opt in ["-t", "--template"]:
            args['template'] = val
        elif opt in ["-h", "--help"]:
            usage("Help for this script")

    if len(remainder) > 0:
        usage("Unknown option(s) specified: <%s>" % remainder[0])
    if not os.path.exists(args['topicsdir']):
        usage("topics dir specified does not exist or is inaccessible")
    if not os.path.exists(args['intro']):
        usage("intro html file specified does not exist or is inaccessible")
    if not os.path.exists(args['template']):
        usage("template file specified does not exist or is inaccessible")

    return args


def do_main():
    '''entry point'''
    args = get_args()
    template = get_file_contents(args['template'])
    intro = get_file_contents(args['intro'])
    topics = yaml.safe_load(get_topic_contents(args['topicsdir']))
    put_html_header()
    put_intro(intro)
    for topic in topics:
        put_topic_start(topic)
        for entry in topics[topic]:
            put_entry(entry['entry'], template)
        put_topic_end()
    put_html_footer()


if __name__ == '__main__':
    do_main()
