FROM openjdk:7-alpine as builder
RUN apk add --no-cache \
		python2-dev \
		git \
		py2-pip \
		py2-openssl \
		py-twisted \
		py2-yaml \
		protobuf-dev \
		bash && \
	pip install --no-cache-dir \
		wheel \
		protobuf==2.6.1 && \
	git clone https://github.com/WithSecureLabs/drozer/ /tmp/drozer && \
	cd /tmp/drozer && \
	python setup.py bdist_wheel

FROM openjdk:7-jre-alpine
RUN --mount=target=/builder,from=builder,source=/tmp/drozer/dist apk add --no-cache \
		py2-pip \
		py2-openssl \
		py-twisted \
		py2-yaml && \
	pip install --no-cache-dir \
		protobuf==2.6.1 \
		service_identity && \
	pip install /builder/drozer*.whl --no-cache-dir && \
	apk del --no-cache \
		py2-pip
ENTRYPOINT ["drozer"]