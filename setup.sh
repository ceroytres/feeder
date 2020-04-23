#!/bin/bash

apt-get update && sudo apt-get install ffmpeg build-essential cmake \
                                  libopenblas-dev liblapack-dev \
                                  libx11-dev libgtk-3-dev 

cd v4l2loopback && make && sudo make install

pip install -r ./requirements.txt