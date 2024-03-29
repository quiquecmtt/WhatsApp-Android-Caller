﻿# WhatsApp-Android-Caller
Simple python application that keeps calling a contact through WhatsApp with all adb connected devices.  

## Software Preparation
For this program to work, `adb` must be installed. Refer to this [link](https://www.xda-developers.com/install-adb-windows-macos-linux/) to install it.  

Execute the following commands to download the repository and install the python modules required
```console
$ git clone https://github.com/Quik-e/WhatsApp-Android-Caller.git
$ cd WhatsApp-Android-Caller
$ pip3 install -r requirements.txt
```

Execute `gui.py` to run the app.
```console
$ python3 gui.py
```
## Hardware preparation
Connection between the phone and the PC can be done in two ways:
- Through a USB cable and allowing PC to control device.
- Through Wi-Fi with `adb connect`. Refer to this [link](https://developer.android.com/studio/command-line/adb).
