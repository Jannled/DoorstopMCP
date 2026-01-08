# Doorstop MCP
Quick and dirty implementation of a [MCP Server](https://github.com/modelcontextprotocol/python-sdk) for the Python [Doorstop framework](https://github.com/doorstop-dev/doorstop).


| Port             | Description                                                              |
| ---------------- | ------------------------------------------------------------------------ |
| 3001             | The DoorstopMCP server                                                   |
| 7867             | A tweaked version of the doorstop-server that will update on page reload |
| 6274, 6277, 3002 | Port of MCP Explorer when Docker was started with `--profile inspector`  |


## Quickstart
> [!NOTE]  
> This tool is not yet ready for production use, as there is no user authentication. 
> Please only use the MCP server in a trusted network.

### With Docker
```bash
# Standard
docker compose up --force-recreate

# With MCP Explorer. Check the console for the link to the local page
docker compose up --force-recreate --profile inspector
```

### With VS Code
```bash
# Create the (local) repo where the requirements are tracked
mkdir reqs
cd reqs
git init

# Create all documents you need, e.g.
doorstop create REQ ./reqs/req
doorstop create LLR ./reqs/llr --parent REQ
doorstop create TST ./reqs/tests --parent REQ
```

Then in the Run and Debug (Ctrl+Shift+D) pane start the _Python Debugger: Module_ launch target.

## Testing the API
You can explore the MCP by using the following web GUI:

```bash
npx -y @modelcontextprotocol/inspector
```

Options:
- Transport Type: Streamable HTTP
- URL: [localhost:3001/mcp](http://localhost:3001/mcp)
- Connection Type: Via Proxy

## Vibe CLI Configuration
To use this MCP server with the Vibe CLI, add the following to your configuration:

```toml
[[mcp_servers]]
name = "doorstop"
transport = "streamable-http"
url = "http://localhost:3001/mcp"
```
## Antigravity MCP Configuration
```json
{
	"mcpServers": {
		"doorstop": {
			"serverUrl": "http://localhost:3001/mcp"
		}
	}
}
```
## Custom Attributes
Some attributes commonly used in requirements engineering such as Functional / Non-Functional
requirements are an afterthought in Doorstop and have to be 
[added manually](https://doorstop.readthedocs.io/en/latest/reference/item.html#extended-item-attributes)
by the user of the framework. Here is the list of attributes that where extended by this
MCP server. They are automatically added to every document and when creating an item they can
be populated.

| Attribute       | Examples                                                    |
| --------------- | ----------------------------------------------------------- |
| `type`          | Functional, Non-Functional or Constraint                    |
| `review-method` | Review by Design, Test, Inspection, Analysis, Demonstration |

An example of how they are added to every .doorstop.yml file:

```yml
# [...]
attributes:
  reviewed:
    - type
    - verification-method
```

## Undocumented attributes for html export
Also currently lacking from the documentation are the attributes that tweak some fields in
the html exported version. See the following example from the [reqs of the doorstop
project](https://github.com/doorstop-dev/doorstop/blob/develop/reqs/.doorstop.yml):

```yml
settings:
  digits: 3
  prefix: REQ
  sep: ''
attributes:
  defaults:
    doc:
      name: 'Requirements'
      title: 'Requirements for _Doorstop_'
      ref: 'REQ-DS-2024'
      by: 'Wfg'
      major: '1'
      minor: 'A'
      copyright: 'Doorstop'
```

## Implementation Status
- [ ] ~~create: create a new document directory~~
- [ ] ~~delete: delete a document directory~~
- [ ] add: create an item file in a document directory
- [ ] ~~remove: remove an item file from a document directory~~
- [ ] edit: open an existing item or document for editing
- [ ] reorder: organize the outline structure of a document
- [ ] link: add a new link between two items
- [ ] ~~unlink: remove a link between two items~~
- [ ] clear: absolve items of their suspect link status
- [ ] review: absolve items of their unreviewed status
- [ ] ~~import: import an existing document or item~~
- [ ] ~~export: export a document as YAML or another format~~
- [ ] ~~publish: publish a document as text or another format~~

Not implementing delete operations for now. And import/export/publish is not useful for an MCP server. 
