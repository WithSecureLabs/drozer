FROM openjdk:7u221-slim-jessie
RUN apt-get update && \
	apt-get install \
		python \
		python-pip \
		python-protobuf \
		python-openssl \
		python-twisted \
		python-yaml \
		git \
		protobuf-compiler \
		libexpat1 \
		libexpat1-dev \
		libpython-dev \
		libpython2.7 \
		libpython2.7-dev \
		python-dev \
		python2.7-dev \
		-y
RUN git clone https://github.com/mwrlabs/drozer/ /tmp/drozer
RUN cd /tmp/drozer && \
	make deb
RUN dpkg -i /tmp/drozer/dist/drozer*.deb
