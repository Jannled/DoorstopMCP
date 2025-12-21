import logging
from typing import cast

import doorstop
from doorstop import Document, DoorstopError, Tree
from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

doorstop_root = 'test'

mcp = FastMCP(
    'DoorstopMCP',
    json_response=True,
    debug=True,
    host='0.0.0.0',
    port=3001
)

@mcp.resource('doorstop://version')
def get_doorstop_version():
    """Get the version of the underlying Doorstop Framework"""

    return doorstop.__version__


@mcp.resource('doorstop://list_documents')
def list_documents() -> list[Tree]:
    """
    List all defined documents
    
    :return: A list of documents
    """

    tree = get_tree()
    return cast(list[Tree], tree.documents)


@mcp.resource('doorstop://find_document/{prefix}')
def find_document(prefix: str) -> Document:
    """
    Docstring for find_document
    
    :param prefix: Description
    """

    tree = get_tree()
    document = tree.find_document(prefix)

    return document


@mcp.tool()
def create_item(prefix: str, text: str, header: str|None):
    tree = get_tree()
    item = tree.add_item(value=prefix)
    item.header = header
    item.text = text
    item.save()


def get_tree():
    tree = doorstop.build(root=doorstop_root)
    return tree


# Run with streamable HTTP transport
if __name__ == "__main__":

    try:
        # Dry run to check if Doorstop dir is healthy
        get_tree()

        # Start the MCP Server
        mcp.run(transport="streamable-http")
    
    except DoorstopError as e:
        logging.error(e)
        logging.error('This might indicate that no version control system is configured for this directory.')

    except KeyboardInterrupt:
        logging.info('Keyboard interrupt, exiting...')
