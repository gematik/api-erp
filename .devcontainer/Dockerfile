FROM mcr.microsoft.com/devcontainers/base:bullseye

# Install dependencies required for asciidoctor and Asciidoctor Diagram
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ruby \
        ruby-dev \
        build-essential \
        graphviz \
        plantuml \
        python3 \
        python3-pip \
    && gem install asciidoctor -v 2.0.20 \
    && gem install asciidoctor-diagram -v 2.2.14 \
    && gem install asciidoctor-reducer \
    && pip3 install matplotlib \
    && pip3 install pandas \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Optional: Set the default command for the container
CMD ["bash"]