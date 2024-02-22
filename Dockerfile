FROM ubuntu:jammy-20230425

ENTRYPOINT /bin/bash
RUN apt update
RUN apt install \
    python3 \
    python3-pip \
    python3-protobuf \
    python3-openssl \
    python3-twisted \
    python3-yaml \
    python3-distro \
    git \
    protobuf-compiler \
    libexpat1 \
    libexpat1-dev \
    libpython3-dev \
    python-is-python3 \
    zip \
    default-jdk \
    adb \
    -y

COPY / /tmp
RUN cd /tmp && \
    python setup.py bdist_wheel
RUN pip install /tmp/dist/drozer*.whl
RUN pip install --upgrade protobuf