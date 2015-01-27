from reportlab import platypus
from reportlab.platypus import Flowable

from facturapdf import DefaultStyling


class SimpleLine(Flowable):
    def __init__(self, width, height=0):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def __repr__(self):
        return "SimpleLine (w=%s)" % self.width

    def draw(self):
        self.canv.line(0, self.height, self.width, self.height)


class Paragraph(platypus.Paragraph):
    """
    Identical to Reportlab Paragraph but uses
    a default style. Instead of specifying every time the style
    you just change next_style property until you want to change it again
    """
    next_style = DefaultStyling().invoice_text

    def __init__(self, text, style=None, bulletText=None, frags=None, caseSensitive=1, encoding='utf8'):
        style = style or self.next_style
        platypus.Paragraph.__init__(self, text, style, bulletText, frags, caseSensitive, encoding)

