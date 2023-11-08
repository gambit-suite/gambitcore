# Software installation, no database files
FROM mambaorg/micromamba:jammy as app_base

LABEL base.image="mambaorg/micromamba:0.27.0"
LABEL dockerfile.version="1"
LABEL software="gambitcore"
LABEL software.version=${gambitcore_SOFTWARE_VERSION}
LABEL description="How complete is an assembly compared to the core genome of its species?"
LABEL website="https://github.com/gambit-suite/gambitcore"
LABEL license="https://github.com/gambit-suite/gambitcore/blob/master/LICENSE"
LABEL maintainer1="Andrew Page"
LABEL maintainer.email1="andrew.page@theiagen.com"

# Environment
ENV LC_ALL=C.UTF-8
USER root

# Install mamba environment
COPY --chown=$MAMBA_USER:$MAMBA_USER env.yaml /tmp/env.yaml
RUN micromamba install -y -n base -f /tmp/env.yaml && \
    micromamba clean --all --yes

ARG MAMBA_DOCKERFILE_ACTIVATE=1  # Subsequent RUN commands use environment

RUN micromamba install -c conda-forge -y zlib sqlite
RUN micromamba install -c bioconda -c conda-forge -y gambit

# Install gambitcore
ADD . /gambitcore
WORKDIR /gambitcore
RUN pip3 install .

# Make sure conda, python, and gambitcore are in the path
ENV PATH="/opt/conda/bin:${PATH}"
