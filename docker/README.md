# Description

This is a Docker image that uses OpenJDK 7 to compile and run the drozer computer agent. The official `openjdk:7u221-slim-jessie` Docker image is used as the base image, which can be found here: https://hub.docker.com/layers/openjdk/library/openjdk/7u221-slim-jessie/images/sha256-dc71e8d2c255f0bef75e42a124ceccf3555588abf69b2511781b112ea905f7f1?context=explore

# Build and Install

If you want to build this container yourself, use the `docker build` command to build the Docker container:

`docker build -t fsecurelabs/drozer .`

Alternatively, use the pre-built Docker container at <pending>:

`https://hub.docker.com/r/fsecurelabs/drozer`

# Run and Connect
  
## Option 1: connect to the phone via network

First, obtain a shell into the container:

`docker run -it fsecurelabs/drozer_docker`

Then run the Drozer command to connect to the phone:

`drozer console connect --server <phone IP address>`

## Option 2: connect to the phone via USB

First, forward port 31415 to the phone via ADB:

`adb forward tcp:31415 tcp:31415`

Next, obtain a shell into the container while adding an address to the container's Hosts file:

`docker run -it --add-host host.docker.internal:host-gateway fsecurelabs/drozer_docker`

Finally, connect to drozer:

`drozer console connect --server host.docker.internal`
