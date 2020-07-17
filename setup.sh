#!/bin/bash
set -x
sudo apt-get update && sudo apt-get install -y ffmpeg build-essential cmake \
                                  libopenblas-dev liblapack-dev \
                                  libx11-dev libgtk-3-dev 

cd v4l2loopback && make && sudo make install

sudo depmod -a && sudo modprobe v4l2loopback 

cd ..

pip install -r ./requirements.txt
