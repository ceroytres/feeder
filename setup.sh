#!/bin/bash

sudo apt-get update && sudo apt-get install -y ffmpeg build-essential cmake \
                                  libopenblas-dev liblapack-dev \
                                  libx11-dev libgtk-3-dev 

cd v4l2loopback && make && sudo make install

cd ..
pip install -r ./requirements.txt