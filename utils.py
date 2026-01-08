from datetime import datetime
from typing import cast
import doorstop # type: ignore
from doorstop import Document, Tree # type: ignore

# Keys of the custom attributes added to the requirement yml files
CUSTOM_ATTRIB_TYPE = 'type'
CUSTOM_ATTRIB_VERIFICATION_METHOD = 'verification-method'
CUSTOM_ATTRIBS = [CUSTOM_ATTRIB_TYPE, CUSTOM_ATTRIB_VERIFICATION_METHOD]

PREFIX_MAP = {
	'EXT': 'Extension',
	'HLTC': 'High-level test cases',
	'LLR': 'Low-level Requirements',
	'REQ': 'Requirements',
	'SRD': 'Software Requirements Document',
	'TST': 'Test'
	# You will need to tweak the files manually anyways, but there are probably a ton more
}

DEFAULT_AUTHOR = 'Foo'
DEFAULT_PROJECT = 'Your Project'
DEFAULT_PROJECT_SHORT = 'YP'
DEFAULT_ORGANIZATION = 'Your Organization'

def get_tree(doorstop_root: str) -> Tree:
	"""Helper to load the Requirement tree from disk and run validation."""
	tree = doorstop.build(root=doorstop_root)
	return tree


def add_custom_attribs(tree: Tree):
	"""
	The commonly used attributes `type` (e.g. Functional / Non-Functional) and 
	`review-method` (e.g. Review by Design, Test, ...) are not designed into the Doorstop
	framework and have to be added manually.
	
	:param tree: Description
	"""
	# Iterate over all Documents in the Tree
	for document in cast(list[Document], tree.documents):

		# Add the custom attributes to the Document
		for customAttrib in CUSTOM_ATTRIBS:
			if customAttrib not in document.extended_reviewed:
				document.extended_reviewed.append(customAttrib)

		# Make sure that attributes.defaults exist and is a dict
		if document._attribute_defaults is None: # type: ignore
			document._attribute_defaults = {} # type: ignore
		
		# Add the html attributes to the Document
		if 'doc' not in document._attribute_defaults: # type: ignore
			name = PREFIX_MAP.get(document.prefix, document.prefix)

			document._attribute_defaults['doc'] = { # type: ignore
				'name': name,
				'title': f'{name} for _{DEFAULT_PROJECT}_',
				'ref': f'{document.prefix}-{DEFAULT_PROJECT_SHORT}-{datetime.today().year}',
				'by': DEFAULT_AUTHOR,
				'major': '1',
				'minor': 'A',
				'copyright': DEFAULT_ORGANIZATION
			}

		# Flush the data to disk
		document.save()
