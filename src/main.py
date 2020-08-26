from svglib import svglib
import lxml.etree
import re


indentation = 0
attribute_name = re.compile('(?:\{.*\})?(\w+)')


def prn(value):
    print(' ' * indentation + str(value))


def rawname(key):
    match = attribute_name.match(key)
    if not match:
        raise ValueError('non-matching attribute key [' + key + ']')
    return match[1]


def info(element):
    prn(rawname(element.tag) + ' {')
    global indentation
    indentation += 4
    for key in element.keys():
        prn(rawname(key) + ': [' + str(element.get(key)) + ']')
    for sub in element:
        info(sub)
    indentation -= 4
    prn('}')


fish = svglib.load_svg_file('svgfish.svg')
info(fish)
