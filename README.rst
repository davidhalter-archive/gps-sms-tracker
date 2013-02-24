===================================
GPS/SMS tracking with Fusion Tables
===================================

**Be aware: This is just a proof of concept.**

SMS GPS tracking

Installation
============

Basically you need:

- gammu
- python-gammu

You can install those packages with::

    sudo apt-get install gammu python-gammu

To use gammu (for receiving SMS) you need to configure it.

You can use `gammu-detect` for that. It's really easy to find a configuration
with it, e.g. this is mine::

    [gammu]
    device = /dev/ttyACM3
    name = SAMSUNG_Electr 680e
    connection = at

Register Google Account for Fusion Tables
-----------------------------------------
Enable google api access:

- goto https://code.google.com/apis/console
- ("create")
- enable fusion tables api
- gogo API Access and Create an OAuth 2.0 client ID

  - Call the new project (Client ID) tracker
  - Choose "Installed application"
  - Create client ID

- Take this client id and feed it 
