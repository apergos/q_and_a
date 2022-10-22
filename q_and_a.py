#!/usr/bin/python3
import os
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
    print('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">')
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

    
def do_main():
    '''entry point'''
    template = get_file_contents('QandA.templ')
    intro = get_file_contents('Intro.html')
    topics = yaml.safe_load(get_topic_contents('topics'))
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

