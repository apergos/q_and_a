#!/usr/bin/python3
'''
given a little directory with a topic, questions, answers etc
and a formatting template for these, produce one page of html
'''
import os
import sys
import re
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


def put_topic_start(topic):
    '''write the topic section header with markup to stdout'''
    # FIXME this should not be hardcoded
    print('<details>\n<summary>' + topic + '</summary>\n\n<dl>\n')


def put_topic_end():
    '''write the close topic markup to stdout'''
    # FIXME this should not be hardcoded
    print('</dl>\n</details>\n')


def put_entry(entry, templ, templ_keys):
    '''write out a question with formatting to stdout'''
    mapping = {}
    for templ_key in templ_keys:
        mapping[templ_key] = entry[templ_key]
    print(templ % mapping)


def get_template_keys(content):
    '''
    generate a list of all strings in the template
    file with "%(string-here)s", and return it
    '''
    templ_keys = []
    for line in content.split('\n'):
        expr = r'%\(([^)]*)\)s'
        result = re.search(expr, line)
        if result:
            templ_keys.append(result.group(1))
    return list(set(templ_keys))


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
                  [--footer <path>] |  --help

This script takes a little pile of topics and a list of questions and other
items associated with each question such as reading links and exercises, and
 turns them into one html  page for viewing.

Arguments:
  --dir       (-d):  directory where topic files are located
                     default: ./topics
  --tmeplate  (-t):  path to html template into which the text for each question and related
                     items will be inserted
                     default: ./QandA.templ
  --intro     (-i):  path to a file of introductory text, html formtted, which will be
                     written before the topic questions
                     default: ./html/Intro.html
  --footer    (-f):  path to a file containing the html footer which will be written
                     after the topic questions
                     default: ./html/Footer.html
  --help      (-h):  display this help message

Setup:
  Make sure you have your topic files in the format given in the sample.yaml file
  and that the file names are numbered in the order you would like them to appear
  in the html output.

  The template used for each entry in a topic should have %(name-here)s in each
  location where a string is to be substituted in from the yaml topic file, one
  entry per line. This script will not properly process template files with more
  than one such entry per line.

   See QandA.templ for a sample template file.
"""
    sys.stderr.write(usage_message)
    sys.exit(1)


def validate_args(args, remainder):
    '''check that the args we have are good, whine otherwise'''
    if len(remainder) > 0:
        usage("Unknown option(s) specified: <%s>" % remainder[0])
    if not os.path.exists(args['topicsdir']):
        usage("topics dir specified does not exist or is inaccessible")
    if not os.path.exists(args['intro']):
        usage("intro html file specified does not exist or is inaccessible")
    if not os.path.exists(args['footer']):
        usage("footer html file specified does not exist or is inaccessible")
    if not os.path.exists(args['template']):
        usage("template file specified does not exist or is inaccessible")


def get_args():
    '''get, validate and return args, overriding defaults as needed'''
    args = {'template': 'QandA.templ', 'footer': 'html/Footer.html',
            'intro': 'html/Intro.html', 'topicsdir': 'topics'}
    try:
        (options, remainder) = getopt.gnu_getopt(
            sys.argv[1:], "d:f:i:t:h", ["dir=", "intro=", "footer=",
                                      "template=", "help"])
    except getopt.GetoptError as err:
        usage("Unknown option specified: " + str(err))

    for (opt, val) in options:
        if opt in ["-d", "--dir"]:
            args['topicsdir'] = val
        elif opt in ["-i", "--intro"]:
            args['intro'] = val
        elif opt in ["-f", "--footer"]:
            args['footer'] = val
        elif opt in ["-t", "--template"]:
            args['template'] = val
        elif opt in ["-h", "--help"]:
            usage("Help for this script")

    validate_args(args, remainder)

    return args


def do_main():
    '''entry point'''
    args = get_args()
    template = get_file_contents(args['template'])
    keys = get_template_keys(template)
    topics = yaml.safe_load(get_topic_contents(args['topicsdir']))

    intro = get_file_contents(args['intro'])
    print(intro)

    for topic in topics:
        put_topic_start(topic)
        for entry in topics[topic]:
            put_entry(entry['entry'], template, keys)
        put_topic_end()

    footer = get_file_contents(args['footer'])
    print(footer)


if __name__ == '__main__':
    do_main()
