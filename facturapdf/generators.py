import re
from reportlab import platypus
from facturapdf import flowables, helper


def element(item):
    elements = {
        'framebreak': platypus.FrameBreak,
        'simpleline': flowables.SimpleLine,
        'paragraph': flowables.Paragraph,
        'image': helper.get_image,
    }

    match = re.search('(?P<name>\w+)(\[(?P<args>.+)\])?', item)

    if match and match.group('name') in elements:
        args = [] if not match.group('args') else match.group('args').split(',')
        return elements[match.group('name')](*args)

    return item
