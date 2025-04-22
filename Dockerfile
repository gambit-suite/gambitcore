FROM python:3.10-slim

LABEL software="gambitcore"
LABEL description="Core genome completeness analysis"
LABEL website="https://github.com/gambit-suite/gambitcore"
LABEL license="MIT"
LABEL maintainer="Andrew Page <andrew.page@theiagen.com>"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LC_ALL=C.UTF-8

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc-10 \
    g++-10 \
    zlib1g-dev \
    curl \
    git \
    ca-certificates \
    procps \
 && rm -rf /var/lib/apt/lists/*

# Set GCC 10 as default
RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-10 100 \
 && update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-10 100

# Upgrade pip and install gambit + numpy
RUN pip install --upgrade pip setuptools wheel \
 && pip install https://github.com/jlumpe/gambit/archive/refs/tags/v1.1.0.tar.gz

# Copy and install gambitcore
WORKDIR /gambitcore
COPY . /gambitcore
RUN pip install .

# Set working directory
WORKDIR /data
