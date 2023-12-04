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
    && gem install asciidoctor-diagram -v 2.2.14 \
    && gem install asciidoctor-reducer \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Copy keybinding and task configuration files to the container's .vscode directory
# COPY .vscode/tasks.json .vscode/keybindings.json /workspace/.vscode/

# Set the default command to execute
CMD ["bash"]
