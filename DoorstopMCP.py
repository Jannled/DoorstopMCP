import logging

import doorstop # type: ignore
from doorstop import Document, DoorstopError # type: ignore
from fastmcp import FastMCP

from utils import CUSTOM_ATTRIB_TYPE, CUSTOM_ATTRIB_VERIFICATION_METHOD, add_custom_attribs, get_tree

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

doorstop_root = ''

mcp = FastMCP(
    'DoorstopMCP',
    json_response=True,
    #debug=True,
    host='0.0.0.0',
    port=3001
)

@mcp.tool('doorstop://version')
def get_doorstop_version():
    """Get the version of the underlying Doorstop Framework"""

    return doorstop.__version__


@mcp.tool('doorstop://documents')
def list_documents() -> str:
    """
    List all defined documents
    
    :return: A list of documents
    """

    tree = get_tree(doorstop_root)
    return tree.draw(encoding='UTF-8', html_links=False)


@mcp.tool('doorstop://find_document/{prefix}')
def find_document(prefix: str) -> dict:
    """
    Find a Folder by Short Prefix (e.g. REQ, LLR, TST)
    
    :param prefix: Description
    """

    tree = get_tree(doorstop_root)
    document = tree.find_document(prefix)

    # Return a serializable dictionary instead of the raw Document object
    return {
        "prefix": document.prefix,
        "path": document.path,
        "sep": document.sep,
        "digits": document.digits,
    }


@mcp.tool()
def create_item(
        prefix: str, 
        text: str, 
        req_type: str|None = None,
        verification_method: str|None = None,
        header: str|None = None
    ):
    """
    Create an item like a Requirement, Low Level Requirement or Test
    
    :param prefix: The item prefix to use e.g. REQ, LLR, TST etc.
    :param text: The actual requirement like "The system **shall** do something"
    :param req_type: The Type of the Requirement. Functional, Non-Functional or Constraint
    :param verification_method: E.g. Review by Design, Test, Inspection, Analysis, Demonstration etc.
    :param header: A short title displayed when browsing all items
    """

    # Create a new Item and add Title and Text
    tree = get_tree(doorstop_root)
    item = tree.add_item(value=prefix)
    item.header = header
    item.text = text

    # Type and Verification method need to be added as custom attributes
    item.set(CUSTOM_ATTRIB_TYPE, req_type)
    item.set(CUSTOM_ATTRIB_VERIFICATION_METHOD, verification_method)

    # Flush the data to disk
    item.save()


@mcp.tool('doorstop://items/{prefix}')
def list_items(prefix: str):
    """
    List all items in a document with details
    
    :param prefix: The document prefix (e.g. REQ, TST)
    :return: List of item dictionaries
    """
    tree = get_tree(doorstop_root)
    document = tree.find_document(prefix)

    items = []
    for item in document.items:
        item_data = {
            "uid": str(item),
            "level": str(item.level),
            "header": item.header,
            "text": item.text,
            "normative": item.normative,
            "attributes": {
                "type": item.get(CUSTOM_ATTRIB_TYPE),
                "verification_method": item.get(CUSTOM_ATTRIB_VERIFICATION_METHOD)
            }
        }
        items.append(item_data)
            
    return items


# Run with streamable HTTP transport
if __name__ == "__main__":
    try:
        # Dry run to check if Doorstop dir is healthy
        add_custom_attribs(get_tree(doorstop_root))

        # Start the MCP Server
        mcp.run(transport="streamable-http")
    
    except DoorstopError as e:
        logging.error(e)
        logging.error('This might indicate that no version control system is configured for this directory.')

    except KeyboardInterrupt:
        logging.info('Keyboard interrupt, exiting...')
