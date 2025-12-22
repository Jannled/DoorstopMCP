# Using an official Python Debian image as a baseline
# https://hub.docker.com/_/python
# https://www.debian.org/releases/
FROM python:3.13-slim

# Labels as per:
# https://github.com/opencontainers/image-spec/blob/main/annotations.md#pre-defined-annotation-keys
LABEL org.opencontainers.image.authors="Jannled"
LABEL org.opencontainers.image.version="0.0.1"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.description="Doorstop with MCP"
LABEL org.opencontainers.image.source="https://github.com/Jannled/DoorstopMCP"

# Yeet the apt-cache afterwards, since it is no longer needed
RUN apt-get update && apt-get install -y nano htop git less && rm -rf /var/lib/apt/lists/*

# Create a non root user for enhanced security
RUN groupadd -r door && useradd -r -g door door

# Change workdir to folder where doorstop will be installed (affects COPY, RUN etc.)
WORKDIR /usr/src/doorstop
RUN git config --global --add safe.directory /usr/src/doorstop

# Install all Python libs that are required (installing under the root user, since the other user has no home)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set the ownership and permissions for the application files, switch to this user for the rest of the script
RUN chown -R door:door /usr/src/doorstop
USER door

# Copy the MCP code
COPY . .
RUN mkdir reqs && cd reqs && git init
RUN doorstop create REQ ./reqs/req
RUN doorstop create LLR ./reqs/llr --parent REQ
RUN doorstop create TST ./reqs/tests --parent REQ

VOLUME [ "/usr/src/doorstop/reqs" ]

# Exposes the port that FastMCP is listening to
EXPOSE 3001

# Run the FastMCP server when the container launches
CMD ["python", "-m", "DoorstopMCP"]
