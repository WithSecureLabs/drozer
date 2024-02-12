# drozer

## ----------------------------------------------------------------

## NOTE

This is an BETA release of a rewritten drozer version, this version is updated to support python3.

Currently, the following known issues are present:

- Building of custom agents functionality will crash the drozer client, this functionality is considered out of scope for the beta release of the revived drozer project.
- It is not possible to run drozer on a Windows host; you must run drozer on either a virtual machine or Docker image

## ----------------------------------------------------------------

drozer is an security testing framework for Android.

drozer allows you to search for security vulnerabilities in apps and devices by assuming the role of an app and interacting with the Android Runtime, other apps' IPC endpoints and the underlying OS.

drozer provides tools to help you use, share and understand public Android exploits.

drozer is open source software, maintained by WithSecure, and can be downloaded from: [https://labs.withsecure.com/tools/drozer/](https://labs.withsecure.com/tools/drozer/)

## Operating System Requirements

## Installing

### Software pre-requisites

1. [Python3.8](https://www.python.org/downloads/)

2. [Protobuf](https://pypi.python.org/pypi/protobuf) 4.25.2 or greater

3. [Pyopenssl](https://pypi.python.org/pypi/pyOpenSSL) 22.0.0 or greater 

4. [Twisted](https://pypi.python.org/pypi/Twisted) 18.9.0 or greater

4. [Distro](https://pypi.org/project/distro/) 1.8.0 or greater

5. [Java Development Kit](https://adoptopenjdk.net/releases.html) 11 or greater

## ----------------------------------------------------------------

### Installing (Kali / Debian)

You can use `pip` to install the latest release of drozer:

```
pip install drozer-<version>.whl
```

### Building and Installing (Kali / Debian)

All of thee requirements can be installed via the following command:

```
sudo apt install python3 python3-pip python3-protobuf python3-openssl \
python3-twisted python3-yaml python3-distro git protobuf-compiler \
libexpat1 libexpat1-dev libpython3-dev python-is-python3 zip default-jdk
```

Then build drozer for Python wheel

```
git clone https://github.com/WithSecureLabs/drozer.git
cd drozer
python setup.py bdist_wheel
```
Finally, install drozer

```
pip install dist/drozer-<version>-py3-none-any.whl
```

===========================

### Building and Installing (Arch Linux/BlackArch)

On any arch based installation, until proper pkgbuilds and pip packages are created, please use an [virtualenv](https://wiki.archlinux.org/title/Python/Virtual_environment).

```
git clone https://github.com/WithSecureLabs/drozer.git
cd drozer
virtualenv -p /usr/bin/python3 venv
source venv/bin/activate
python setup.py bdist_wheel
sudo pip install dist/drozer-<version>-py3-none-any.whl
```

===========================

### Installing (Docker)

Make sure your host user has the ability to create and run Docker images. Then run the following commands:

```
git clone https://github.com/WithSecureLabs/drozer.git
cd drozer
docker build -t drozer-docker .
```

===========================

### Protobuf errors

If protobuf complains about the protobuf defintions being out of date. Copy the protobuf definition from [here](https://github.com/WithSecureLabs/mercury-common/tree/48e81d5ae65ec38dbe1e4bfe09548203dcf13384) into common/protobuf.proto

Then run 
```
cd common
protoc --python_out=../src/pysolar/api/ protobuf.proto
```

## ----------------------------------------------------------------

## Usage

### Installing the Agent

drozer can be installed using Android Debug Bridge (adb).

Download the latest drozer Agent [here](https://github.com/WithSecureLabs/drozer-agent/releases/latest).

`$ adb install drozer-agent-x.x.x.apk`

===========================

### Setup for session

You should now have the drozer Console installed on your PC, and the Agent running on your test device. Now, you need to connect the two and you’re ready to start exploring.

We will use the server embedded in the drozer Agent to do this.

You need to set up a suitable port forward so that your PC can connect to a TCP socket opened by the Agent inside the device or emulator. By default, drozer uses port 31415:

`$ adb forward tcp:31415 tcp:31415`

Now, launch the Agent, select the "Embedded Server" option and tap "Enable" to start the server. You should see a notification that the server has started.

===========================

### Start a session - running drozer on host

On your PC, connect using the drozer Console:

`$ drozer console connect`

If using a real device, the IP address of the device on the network must be specified:

`$ drozer console connect --server 192.168.0.10`

===========================

### Start a session - Docker image

You have two options for connecting to the drozer agent.

**Option 1 - network connection**

First start the docker image in interactive mode:

`$ docker run -it drozer_docker`

Then connect to the drozer agent via the Android device's IP address

`$ drozer console connect --server 192.168.0.10`

**Option 2 - USB connection**

First, start the docker image in interactive mode while forwarding TCP traffic from the host to the docker image:

`$ docker run -it --add-host host.docker.internal:host-gateway drozer_docker`

Then connect to the drozer agent via the forwarded host interface:

`$ drozer console connect --server host.docker.internal`

## -------------------------------------------------------------

### Command Reference

You should be presented with a drozer command prompt:

```
selecting f75640f67144d9a3 (unknown sdk 4.1.1)  
dz>
```
The prompt confirms the Android ID of the device you have connected to, along with the manufacturer, model and Android software version.

| Command        | Description           |
| ------------- |:-------------|
| run  | Executes a drozer module
| list | Show a list of all drozer modules that can be executed in the current session. This hides modules that you do not have suitable permissions to run. | 
| shell | Start an interactive Linux shell on the device, in the context of the Agent process. | 
| cd | Mounts a particular namespace as the root of session, to avoid having to repeatedly type the full name of a module. | 
| clean | Remove temporary files stored by drozer on the Android device. | 
| contributors | Displays a list of people who have contributed to the drozer framework and modules in use on your system. | 
| echo | Print text to the console. | 
| exit | Terminate the drozer session. | 
| help | Display help about a particular command or module. | 
| load | Load a file containing drozer commands, and execute them in sequence. | 
| module | Find and install additional drozer modules from the Internet. | 
| permissions | Display a list of the permissions granted to the drozer Agent. | 
| set | Store a value in a variable that will be passed as an environment variable to any Linux shells spawned by drozer. | 
| unset | Remove a named variable that drozer passes to any Linux shells that it spawns. | 

## License

drozer is released under a 3-clause BSD License. See LICENSE for full details.

## Contacting the Project

drozer is Open Source software, made great by contributions from the community.

For full source code, to report bugs, suggest features and contribute patches please see our Github project:

  <https://github.com/WithSecureLabs/drozer>

Bug reports, feature requests, comments and questions can be submitted [here](https://github.com/WithSecureLabs/drozer/issues).
