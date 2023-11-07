# Software installation, no database files
FROM mambaorg/micromamba:jammy as app_base

# get software version from VERSION file

ARG GAMBITTOOLS_SRC_URL=https://github.com/gambit-suite/gambittools/archive/refs/heads/main.zip

LABEL base.image="mambaorg/micromamba:0.27.0"
LABEL dockerfile.version="1"
LABEL software="GAMBITDB"
LABEL software.version=${GAMBITDB_SOFTWARE_VERSION}
LABEL description="Create databases for Gambit"
LABEL website="https://github.com/gambit-suite/gambitdb"
LABEL license="https://github.com/gambit-suite/gambitdb/blob/master/LICENSE"
LABEL maintainer1="Andrew Page"
LABEL maintainer.email1="andrew.page@theiagen.com"
LABEL maintainer2="Michelle Scribner"
LABEL maintainer.email2="michelle.scribner@theiagen.com"

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

# Install GAMBITtools package
RUN pip install ${GAMBITTOOLS_SRC_URL} && \
  micromamba clean -a -y

# Install GAMBITDB
ADD . /gambitdb
WORKDIR /gambitdb
RUN pip3 install .

# Make sure conda, python, and GAMBITDB are in the path
ENV PATH="/opt/conda/bin:${PATH}"

RUN bash /gambitdb/run_tests.sh
