# Description

This is a Docker image that uses OpenJDK 7 to compile and run the drozer computer agent. The official `openjdk:7u221-slim-jessie` Docker image is used as the base image, which can be found here: https://hub.docker.com/layers/openjdk/library/openjdk/7u221-slim-jessie/images/sha256-dc71e8d2c255f0bef75e42a124ceccf3555588abf69b2511781b112ea905f7f1?context=explore

# Build and Install

If you want to build this container yourself, use the `docker build` command to build the Docker container:

`docker build -t <pending> .`

Alternatively, use the pre-built Docker container at <pending>:

`<pending>`

# Run and Connect

First, obtain a shell into the container:

`docker run -it <pending>`

Then run the Drozer command to connect to the phone:

`drozer console connect --server <phone IP address>`
