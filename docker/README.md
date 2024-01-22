# Description

WithSecure's official Docker image for [drozer](https://labs.withsecure.com/tools/drozer)'s computer client.

drozer allows you to search for security vulnerabilities in apps and devices by assuming the role of an app and interacting with the Dalvik VM, other apps' IPC endpoints and the underlying OS. Its primary use case is simulating a rogue application on the device. A penetration tester does not have to develop an app with custom code to interface with a specific content provider. Instead, drozer can be used with little to no programming experience required to show the impact of letting certain components be exported on a device.

This is a Docker image that uses OpenJDK 7 to compile and run the drozer computer agent. The official `openjdk:7-alpine` Docker image is used for the build stage, with `openjdk:7-jre-alpine` acting as the base for the final image.

# Build and Install

A pre-built image can be pulled by running:

```docker pull withsecurelabs/drozer```

Alternatively, to build this container yourself, use the `docker build` command, pointing it towards WithSecure's GitHub repository:

```docker build -t withsecurelabs/drozer https://github.com/WithSecureLabs/drozer.git#develop:docker```

The source Dockerfile is available [here](https://github.com/WithSecureLabs/drozer/blob/develop/docker/Dockerfile).

# Run and Connect

## Option 1: connect to the phone via network

If the target phone and PC are on the same network, this tends to be the easiest approach.

1. Ensure that the drozer agent is running on the target device, and that the embedded server has been started.
2. Then, to run drozer and connect to the phone, run: ```docker run --net host -it withsecurelabs/drozer console connect --server <phone IP address>```

If a system shell is required (for example, to inspect and retrieve any files downloaded by drozer), you can:
1. Ensure that the drozer agent is running on the target device, and that the embedded server has been started.
2. Obtain a shell into the container: ```docker run --net host -it --entrypoint sh withsecurelabs/drozer```
3. Then run the drozer command to connect to the phone: ```drozer console connect --server <phone IP address>```

## Option 2: connect to the phone via USB

If network communications is restricted, `adb` port forwarding can be used to forward TCP traffic via USB.

1. First, forward port 31415 to the phone via ADB: ```adb forward tcp:31415 tcp:31415```
2. Ensure that the drozer agent is running on the target device, and that the embedded server has been started.
3. Then, to run drozer and connect to the phone, run: ```docker run --net host -it withsecurelabs/drozer console connect --server localhost```

If a system shell is required (for example, to inspect and retrieve any files downloaded by drozer), you can:
1. First, forward port 31415 to the phone via ADB: ```adb forward tcp:31415 tcp:31415```
2. Ensure that the drozer agent is running on the target device, and that the embedded server has been started.
3. Obtain a shell into the container: ```docker run --net host -it --entrypoint sh withsecurelabs/drozer```
4. Then run the drozer command to connect to the phone: ```drozer console connect --server localhost```

# Usage

Refer to the [drozer README.md](https://github.com/WithSecureLabs/drozer/blob/develop/README.md#usage) and [Wiki](https://github.com/WithSecureLabs/drozer/wiki) on GitHub.
