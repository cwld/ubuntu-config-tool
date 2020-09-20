# ubuntu-config-tool

This is a python simple tool that will install packages and copy files to deploy an application on a debian based system.
The tool will first install the packages, then copy the files, then start (or restart) the service.

## Configuration

The configuration is a single yaml file with the format below:

```
---
packages:
  install:
    - <packages to install as listed in aptitude>
  remove:
    - <packages to remove as listed in aptitude>

files:
  - <name>:
      source: <relative or absolute path to copy files from>
      destination: <relative or absolute path to copy files to>
      requiresRestart <true if service must be restarted on update, false if restart not required>
      access:
        owner: <destination file(s) owner>
        group: <destination file(s) group>
        mode: <destination file(s) mode in octal format>

service:
  startCommand: <command used to start the service>
  restartCommand: <command used to restart the service>
```

### Packages

The packages section in the configuration will indicate which packages to install and/or remove, and takes a list of packages as you would specify using apt-get.
For example, if you were to install nginx and remove apache2, your config would look like this:

```
packages:
  install:
    - nginx
  remove:
    - apache2
...
```
Note, package installation will not restart the service as it is assumed that would be done by the package installer if necessary.
Package management is optional, and either install/remove can be specified or both.

### Files

The files section in the configuration will indicate which files to copy. The files may be a path (folder) in which case the copy will be recursive, or can be single files.
All options must be specified for each file, and you must take care to ensure that paths are not duplicated as order is not guaranteed and files will be overwritten if existing.
For example, if you wanted to overwrite the default nginx index file with your own in a local www directory and have it owned by www-data with read only permissions, your config would look like this:
```
...
files:
  - nginx-default-index:
      source: www/index.html
      destination: /usr/share/nginx/html
      access:
        owner: www-data
        group: www-data
        mode: 444
...
```
File copy is optional, omit this if not required, however if needed then all parameters are mandatory

### Service

This service section in the configuration indicates how the service is to be run and restarted. These commands should be shell command that can be executed and return within a reasonable (ie must control a daemonset).
The restart command will restart the service if any files or packages are updated by this tool, otherwise the start command will be called to ensure the service is running.
For example, if you wanted to launch nginx, your config would look like this:
```
...
service:
  startCommand: 'service nginx start'
  restartCommand: 'service nginx restart'
```
If the systemd (or upstart, depending on the version of debian) file is not created during package install, you can write your own and use the files section to copy it to the relevant area.
Service control is optional, omit this if you do not want the service to be started/restarted, however if needed then all parameters are mandatory.

## Installation

Run `./bootstrap.sh` to install any packages required by the tool itself, and then you can run supplied ubuntu-config-tool.

## Usage

To use this tool, simply run: `ubuntu-config-tool -c <your yaml config file>` and the config tool will take care of installing services as necessary.
Installing/removing packages will be processed first, followed by copying and updating files, and then the service will be started or restarted.
