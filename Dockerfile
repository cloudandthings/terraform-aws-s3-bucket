# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.245.0/containers/ubuntu/.devcontainer/base.Dockerfile

# [Choice] Ubuntu version (use ubuntu-22.04 or ubuntu-18.04 on local arm64/Apple Silicon): ubuntu-22.04, ubuntu-20.04, ubuntu-18.04
ARG VARIANT="jammy"
FROM mcr.microsoft.com/vscode/devcontainers/base:0-${VARIANT}

# Install additional OS packages.
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends python3 python3-pip

# python-is-python3
RUN ln -s $(which python3) /usr/bin/python

# terraform-docs
COPY .tfdocs-config.yml .
RUN curl -sSLo ./terraform-docs.tar.gz https://github.com/terraform-docs/terraform-docs/releases/download/v0.16.0/terraform-docs-v0.16.0-linux-amd64.tar.gz
RUN tar -xzf terraform-docs.tar.gz && chmod +x terraform-docs && mv terraform-docs /usr/local/bin/terraform-docs

# tfsec
RUN curl -sSLo ./tfsec.tar.gz https://github.com/aquasecurity/tfsec/releases/download/v1.28.0/tfsec_1.28.0_linux_amd64.tar.gz
RUN tar -xzf tfsec.tar.gz && chmod +x tfsec && mv tfsec /usr/local/bin/tfsec

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY .pre-commit-config.yaml .

COPY .devcontainer/.bashrc_extra .
RUN cat .bashrc_extra >> /home/vscode/.bashrc

# checkov:skip=CKV_DOCKER_2: No need for HEALTHCHECK on local container
# checkov:skip=CKV_DOCKER_3: Use default root & vscode users
