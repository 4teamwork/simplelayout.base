from ftw.builder.archetypes import ArchetypesBuilder
from ftw.builder import builder_registry


class ParagraphBuilder(ArchetypesBuilder):

    portal_type = 'Paragraph'

builder_registry.register('paragraph', ParagraphBuilder)

class PageBuilder(ArchetypesBuilder):

    portal_type = 'Page'

builder_registry.register('sl-page', PageBuilder)
