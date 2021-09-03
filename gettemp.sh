#!/bin/bash
ls -l /sys/bus/w1/devices/28* && cat  /sys/bus/w1/devices/28*/w1_slave || echo "No device!"

