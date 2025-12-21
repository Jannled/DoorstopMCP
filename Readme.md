# Doorstop MCP
Quick and dirty implementation of a [MCP Server](https://github.com/modelcontextprotocol/python-sdk) for the Python [Doorstop framework](https://github.com/doorstop-dev/doorstop).

## Testing the API
You can explore the MCP by using the following web GUI:

```bash
npx -y @modelcontextprotocol/inspector
```

Options:
- Transport Type: Streamable HTTP
- URL: [localhost:3001/mcp](http://localhost:3001/mcp)
- Connection Type: Via Proxy

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
