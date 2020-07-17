#!/bin/bash
sudo modprobe -r v4l2loopback
find "/lib/modules/$(uname -r)" | grep v4l2loopback | sudo xargs rm -v