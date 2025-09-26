# Use the official Debian bullseye image as a parent image
FROM mcr.microsoft.com/devcontainers/base:bullseye

# Install dependencies required for asciidoctor and Asciidoctor Diagram
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ruby \
        ruby-dev \
        build-essential \
        graphviz \
        plantuml \
    && gem install asciidoctor -v 2.0.20 \
    && gem install asciidoctor-diagram -v 2.3.0 \
    && gem install asciidoctor-reducer \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv \
 && rm -rf /var/lib/apt/lists/*

# Then install packages
RUN python3 -m pip install --no-cache-dir --upgrade pip
RUN python3 -m pip install --no-cache-dir PyYAML
RUN python3 -m pip install --no-cache-dir packaging
RUN python3 -m pip install --no-cache-dir requests

# Copy keybinding and task configuration files to the container's .vscode directory
# COPY .vscode/tasks.json .vscode/keybindings.json /workspace/.vscode/

# Set the default command to execute
CMD ["bash"]
