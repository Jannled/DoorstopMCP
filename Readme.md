# Doorstop MCP
Quick and dirty implementation of a [MCP Server](https://github.com/modelcontextprotocol/python-sdk) for the Python [Doorstop framework](https://github.com/doorstop-dev/doorstop).


| Port             | Description                                                              |
| ---------------- | ------------------------------------------------------------------------ |
| 3001             | The DoorstopMCP server                                                   |
| 7867             | A tweaked version of the doorstop-server that will update on page reload |
| 6274, 6277, 3002 | MCP Explorer when Docker was started with `--profile inspector`          |


## Quickstart
> [!WARNING]  
> This tool is not yet ready for production use, as there is no user authentication. 
> Please only use the MCP server in a trusted network.

### With Docker
```bash
docker compose up --force-recreate
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

## Inspecting Results
The container will also start the [doorstop-server](https://doorstop.readthedocs.io/en/latest/web.html) 
in a seperate process so you can inspect your results visually. Originally the html exporter is only
run once, therefore we had to [fork](https://github.com/Jannled/DoorstopMCP) the doorstop project and
adjust it to fetch the document tree on every page reload.

Just navigate to [http://{YOUR_HOSTNAME_IP}:7867](http://localhost:7867) and refresh after every change.

## Testing the API
You can explore the MCP by using the following web GUI from your command line:

```bash
npx -y @modelcontextprotocol/inspector
```

Or by starting a second container with MCP Explorer:

```bash
docker compose up --force-recreate --profile inspector
```

Options for MCP Explorer:
- Transport Type: Streamable HTTP
- URL: [localhost:3001/mcp](http://localhost:3001/mcp)
- Connection Type: Via Proxy

## MCP Clients
Some example configurations to connect your prompting client to this MCP Server.
This list is not exhaustive, feel free to open a pull request with the client that you used:

### Open WebUI Configuration
Create a new External Tool in the admin interface, set the type to `MCP Streamable HTTP`,
the URL to `http://{YOUR_URL}:3001/mcp` and make sure to disable authentication as this is not yet
supported by this MCP Server and will lead to Open WebUI silently ignoring the tool.
You will then need to adjust the permissions/visibility if you want to make this tool available to
non admin users

### Vibe CLI Configuration
To use this MCP server with Mistral Vibe CLI, add the following to your configuration:

```toml
[[mcp_servers]]
name = "doorstop"
transport = "streamable-http"
url = "http://localhost:3001/mcp"
```

### Antigravity MCP Configuration
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
- [x] read all documents
- [x] read all items
- [x] read the doorstop framework version
- [ ] create: create a new document directory
- [ ] delete: delete a document directory
- [x] add: create an item file in a document directory
- [ ] remove: remove an item file from a document directory
- [ ] edit: open an existing item or document for editing
- [ ] reorder: organize the outline structure of a document
- [ ] link: add a new link between two items
- [ ] unlink: remove a link between two items
- [ ] clear: absolve items of their suspect link status
- [ ] review: absolve items of their unreviewed status
- [ ] ~~import: import an existing document or item~~
- [ ] ~~export: export a document as YAML or another format~~
- [x] publish: publish a document as text or another format
- [ ] ability to switch the workspace, so the MCP can work on different projects
