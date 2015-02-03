import re
from reportlab import platypus
from facturapdf import flowables, helper


def element(item):
    elements = {
        'framebreak': {'class': platypus.FrameBreak},
        'simpleline': {'class': flowables.SimpleLine, 'cast': {0: float, 1: float}},
        'paragraph':  {'class': flowables.Paragraph},
        'image':      {'class': helper.get_image, 'cast': {1: float}},
        'spacer':     {'class': platypus.Spacer, 'cast': {0: float, 1: float}}
    }

    if isinstance(item, str):
        match = re.search('(?P<name>\w+)(\[(?P<args>.+)\])?', item)

        if match and match.group('name') in elements:
            flowable = elements[match.group('name')]
            args = [] if not match.group('args') else match.group('args').split('|')

            if 'cast' in flowable:
                for index, cls in iter(flowable['cast'].items()):
                    args[index] = cls(args[index])

            return flowable['class'](*args)

    return item


def chapter(*args):
    return [element(item) for item in args]