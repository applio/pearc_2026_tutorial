FROM mcr.microsoft.com/devcontainers/base:ubuntu

# Update and install dependencies
RUN apt-get update \
    && apt-get install -y \
    && apt-get install -y \
    ca-certificates git \
    make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
    libsqlite3-dev wget curl llvm libncursesw5-dev xz-utils tk-dev \
    libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev \
    vim-tiny openssh-client dnsutils \
    libopenmpi-dev openmpi-bin gzip libprrte-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Download pyenv to install Python
ENV PYENV_ROOT=/opt/pyenv
# use this commented out line if SSL errors are hit on Windows with Zscaler
# RUN git -c http.sslVerify=false clone https://github.com/pyenv/pyenv.git $PYENV_ROOT
RUN git clone https://github.com/pyenv/pyenv.git $PYENV_ROOT

# Compile dynamic bash extension to speed up pyenv
RUN cd $PYENV_ROOT && src/configure && make -C src

# Build Python 3.12.12 by default.
ARG python_version=3.12.12
# Keep Python source files in /usr/local/src
ENV PYTHON_BUILD_BUILD_PATH=/usr/local/src/
ENV LD_LIBRARY_PATH=/usr/local/lib/python3.12/site-packages/dragon/lib/
# Install a Python with a shared object
ENV PYTHON_CONFIGURE_OPTS="--enable-shared"
# Build Python and clean-up downloaded tarball
RUN /opt/pyenv/plugins/python-build/bin/python-build --verbose --keep ${python_version} /usr/local \
    && rm -fr /usr/local/src/Python-${python_version}.tar.*

# Install DragonHPC wheel
# Note: This will need to be updated to add any dragon "extras" that are needed
COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp