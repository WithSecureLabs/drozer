# drozer

drozer (formerly Mercury) is the leading security testing framework for Android.

drozer allows you to search for security vulnerabilities in apps and devices by assuming the role of an app and interacting with the Dalvik VM, other apps' IPC endpoints and the underlying OS.

drozer provides tools to help you use, share and understand public Android exploits. It helps you to deploy a drozer Agent to a device through exploitation or social engineering. Using weasel (MWR's advanced exploitation payload) drozer is able to maximise the permissions available to it by installing a full agent, injecting a limited agent into a running process, or connecting a reverse shell to act as a Remote Access Tool (RAT).

drozer is open source software, maintained by MWR InfoSecurity, and can be downloaded from: [mwr.to/drozer](http://mwr.to/drozer)


## Build Status

### Linux / OSX

#### Develop:

[![Build Status](https://travis-ci.org/mwrlabs/drozer.svg?branch=develop)](https://travis-ci.org/mwrlabs/drozer)

#### Master:

[![Build Status](https://travis-ci.org/mwrlabs/drozer.svg?branch=master)](https://travis-ci.org/mwrlabs/drozer)

### Windows

[![Build status](https://ci.appveyor.com/api/projects/status/9d4f3qx2sn2yf8tm/branch/develop?svg=true)](https://ci.appveyor.com/project/HenryHoggard/drozer/branch/develop)

## Prerequisites

1. [Python2.7](https://www.python.org/downloads/)

**Note: On Windows please ensure that the path to the Python installation and the Scripts folder under the Python installation are added to the PATH environment variable.**

2. [Protobuf](https://pypi.python.org/pypi/protobuf) 2.6 or greater

3. [Pyopenssl](https://pypi.python.org/pypi/pyOpenSSL) 16.2 or greater

4. [Twisted](https://pypi.python.org/pypi/Twisted) 10.2 or greater

5. [Java Development Kit 1.7](http://www.oracle.com/technetwork/java/javase/downloads/java-archive-downloads-javase7-521261.html) 

**Note: On Windows please ensure that the path to javac.exe is added to the PATH environment variable.**

6. [Android Debug Bridge](https://developer.android.com/studio/releases/platform-tools.html)


## Installing

### Building Python wheel

```
git clone https://github.com/mwrlabs/drozer/
cd drozer
python setup.py bdist_wheel

```
### Installing Python wheel

```
sudo pip install drozer-2.x.x-py2-none-any.whl

```

### Building for Debian/Ubuntu/Mint
```
git clone https://github.com/mwrlabs/drozer/
cd drozer
make deb
```

### Installing .deb (Debian/Ubuntu/Mint)

``` 
sudo dpkg -i drozer-2.x.x.deb
```

### Building for Redhat/Fedora/CentOS

```
git clone https://github.com/mwrlabs/drozer/
cd drozer
make rpm
```
### Installing .rpm (Redhat/Fedora/CentOS)

```
sudo rpm -I drozer-2.x.x-1.noarch.rpm
```

### Building for Windows

**NOTE: Windows Defender and other Antivirus software will flag drozer as malware (an exploitation tool without exploit code wouldn't be much fun!). In order to run drozer you would have to add an exception to Windows Defender and any antivirus software. Alternatively, we recommend running drozer in a Windows/Linux VM.**

```
git clone https://github.com/mwrlabs/drozer/
cd drozer
python.exe setup.py bdist_msi

```

### Installing .msi (Windows)

``` 
Run dist/drozer-2.x.x.win-x.msi 

```

### Arch Linux

`yaourt -S drozer`

## Usage

### Installing the Agent

Drozer can be installed using Android Debug Bridge (adb).

Download the latest Drozer Agent [here](https://github.com/mwrlabs/drozer/releases/download/2.3.4/drozer-agent-2.3.4.apk).

`$ adb install drozer-agent-2.x.x.apk`


### Starting a Session

You should now have the drozer Console installed on your PC, and the Agent running on your test device. Now, you need to connect the two and you’re ready to start exploring.

We will use the server embedded in the drozer Agent to do this.

If using the Android emulator, you need to set up a suitable port forward so that your PC can connect to a TCP socket opened by the Agent inside the emulator, or on the device. By default, drozer uses port 31415:

`$ adb forward tcp:31415 tcp:31415`

Now, launch the Agent, select the “Embedded Server” option and tap “Enable” to start the server. You should see a notification that the server has started.

Then, on your PC, connect using the drozer Console:

On Linux:

`$ drozer console connect`

On Windows:

`> drozer.bat console connect`

If using a real device, the IP address of the device on the network must be specified:

On Linux:

`$ drozer console connect --server 192.168.0.10`

On Windows:

`> drozer.bat console connect --server 192.168.0.10`

You should be presented with a drozer command prompt:

```
selecting f75640f67144d9a3 (unknown sdk 4.1.1)  
dz>
```
The prompt confirms the Android ID of the device you have connected to, along with the manufacturer, model and Android software version.

You are now ready to start exploring the device.


### Command Reference

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

  <https://github.com/mwrlabs/drozer>

Bug reports, feature requests, comments and questions can be submitted [here](https://github.com/mwrlabs/drozer/issues).
  
Follow the latest drozer news, follow the project on Twitter:

  [@mwrdrozer](https://twitter.com/mwrdrozer)



