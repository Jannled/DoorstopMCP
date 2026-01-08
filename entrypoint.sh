#!/bin/bash
git config --global --add safe.directory /usr/src/doorstop
doorstop-server --host 0.0.0.0 & python -m DoorstopMCP

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?
