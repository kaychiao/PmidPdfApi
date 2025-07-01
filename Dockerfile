FROM python:3.10-slim

# Build arguments
ARG APP_VERSION=0.1.0

# Set version label
LABEL version=${APP_VERSION}

WORKDIR /app

# COPY dockerfiles/sources/debian-sources.list /etc/apt/sources.list

# Install system dependencies and setup environment in a single layer
RUN apt-get clean && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
    vim less tzdata curl zip unzip && \
    # Set timezone
    ln -snf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone && \
    dpkg-reconfigure --frontend noninteractive tzdata && \
    # Clean up to reduce image size
    apt-get clean && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy configuration files and install requirements
COPY dockerfiles/sources/pip.conf /etc/pip.conf
COPY dockerfiles/sources/requirements.txt /tmp/
RUN pip3 install --no-cache-dir pip --upgrade && \
    pip3 install --no-cache-dir -r /tmp/requirements.txt \
    --index-url=http://bio-pypi.brbiotech.tech/simple/ \
    --extra-index-url=https://pypi.tuna.tsinghua.edu.cn/simple/ \
    --trusted-host bio-pypi.brbiotech.tech \
    --trusted-host pypi.tuna.tsinghua.edu.cn && \
    rm -rf /tmp/requirements.txt /root/.cache/pip/*

# Copy application code
COPY . /app/

# Set environment variables
ENV LANG=C.UTF-8
ENV PYTHONPATH=/app
ENV APP_VERSION=${APP_VERSION}
ENV TZ=Asia/Shanghai

# Expose port
EXPOSE 8091

# Default command
CMD ["sh", "/app/dockerfiles/sh/run_gunicorn.sh", "8091"]