# feeder

# Setup

Clone the repo as follows:

```bash
git clone 
```


```bash 
sudo ./setup.sh # install necessary packages
```

# Run 

Currently, the default dummy device is ```/dev/video2```. You can check if it exists using the following:

```bash
./ls_vid.sh
```
To add more run:

``` bash
modprobe v4l2loopback device=1
```
## Running the DnD roll overlay

```bash
python dnd/dnd_gui.py
```

if using Google Hangouts or Zoom 

```
python dnd/dnd_gui.py -f
```
since they flip the video. 

# Uninstalling v4l2loopback

```
./uninstall.sh
```