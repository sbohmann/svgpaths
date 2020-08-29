from svglib import svglib
import lxml.etree
import re
import svg_path


indentation = 0
attribute_name = re.compile(r'(?:{.*})?(\w+)')


def prn(value):
    print(' ' * indentation + str(value))


def rawname(key):
    match = attribute_name.match(key)
    if not match:
        raise ValueError('non-matching attribute key [' + key + ']')
    return match[1]


def info(element):
    raw_tag = rawname(element.tag)
    prn(raw_tag + ' {')
    global indentation
    indentation += 4
    for key in element.keys():
        raw_key = rawname(key)
        value = str(element.get(key))
        prn(raw_key + ': [' + value + ']')
        if raw_tag == 'path' and raw_key == 'd':
            path = svg_path.parse(value)
            for step in path:
                prn(step)
    for sub in element:
        info(sub)
    indentation -= 4
    prn('}')


fish = svglib.load_svg_file('svgfish.svg')
info(fish)
