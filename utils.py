from typing import cast
import doorstop # type: ignore
from doorstop import Document, Tree # type: ignore

# Keys of the custom attributes added to the requirement yml files
CUSTOM_ATTRIB_TYPE = 'type'
CUSTOM_ATTRIB_VERIFICATION_METHOD = 'verification-method'
CUSTOM_ATTRIBS = [CUSTOM_ATTRIB_TYPE, CUSTOM_ATTRIB_VERIFICATION_METHOD]


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
        
        # Flush the data to disk
        document.save()
