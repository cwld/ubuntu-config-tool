#!/usr/bin/env bash

apt-get -q update
apt-get -q -y install python3 python3-pip
python3 -m pip install --upgrade pip
