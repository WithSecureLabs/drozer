# Description

This is a Docker image that uses OpenJDK 7 to compile and run the drozer computer agent. The official `openjdk:7u221-slim-jessie` Docker image is used as the base image, which can be found here: https://hub.docker.com/layers/openjdk/library/openjdk/7u221-slim-jessie/images/sha256-dc71e8d2c255f0bef75e42a124ceccf3555588abf69b2511781b112ea905f7f1?context=explore

# Build and Install

If you want to build this container yourself, use the `docker build` command to build the Docker container:

`docker build -t fsecurelabs/drozer .`

Alternatively, use the pre-built Docker container at <pending>:

`https://hub.docker.com/r/fsecurelabs/drozer`

# Run and Connect

First, obtain a shell into the container:

`docker run -it fsecurelabs/drozer`

Then run the Drozer command to connect to the phone:

`drozer console connect --server <phone IP address>`

Notes on `phone IP address>`: For an real Android device, the phone and the host machine should be on the same LAN network, and an explicit LAN IP address of the phone should be used, for example

`drozer console connect --server 192.168.7.70`
  
However, for a virtual device, say an Android emulator, port-forwarding must be created and the correct "IP address" must be used in order to successfully connect the Drozer client running in docker to the Drozer Server listening on port 31415(default) of the Android emulator. Specifically, 

- Set up port forwarding

`adb forward tcp:31415 tcp:31415`

- Connect to drozer agent

`drozer console connect --server host.docker.internal`

for more details about [How to access host port from docker container](https://stackoverflow.com/questions/31324981/how-to-access-host-port-from-docker-container).
