#!/bin/bash

apt-get update && apt-get install ffmpeg

cd v4l2loopback && make && sudo make install

pip install -r ./requirements.txt