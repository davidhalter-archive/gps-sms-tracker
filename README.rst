===================================
GPS/SMS tracking with Fusion Tables
===================================

**Be aware: This is just a proof of concept.**

SMS GPS tracking with some devices I don't know the model of.
This is just a proof of concept, I wouldn't recommend to use it.

Installation
============

Basically you need:

- gammu
- python-gammu
- django
- postgresql

You can install those packages with (under **Ubuntu**)::

    ./install.sh

To use gammu (for receiving SMS) you need to configure it.

You can use `gammu-detect` for that. It's really easy to find a configuration
with it, e.g. this is mine::

    [gammu]
    device = /dev/ttyACM3
    name = SAMSUNG_Electr 680e
    connection = at
