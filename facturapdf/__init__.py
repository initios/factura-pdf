from facturapdf.story_builders import DefaultStoryBuilder
from facturapdf.styles import DefaultStyling
from facturapdf.templates import DefaultTemplate
from .flowables import SimpleLine
from .strategies import DefaultStrategy
from .dtos import Customer


class InvoiceGenerator(object):
    def __init__(self, strategy=None, template=None, story_builder=None, data=None):
        """
        data Parameter should be an instance of dtos.Data
        """
        self.strategy = strategy or DefaultStrategy()
        self.template = template or DefaultTemplate()
        self.story_builder = story_builder or DefaultStoryBuilder()
        self.data = data

    def generate(self, destination_file):
        doc = self.template.create_document(destination_file, self.strategy.UNITS)
        story = self.story_builder.create(self.strategy, self.template, self.data)
        doc.build(flowables=story)