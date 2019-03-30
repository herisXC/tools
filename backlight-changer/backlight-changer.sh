#!/bin/bash

while inotifywait -e modify /sys/class/backlight/acpi_video0/brightness; do
	DELL_BRIGHTNESS=`cat /sys/class/backlight/acpi_video0/brightness`
	NV_BRIGHTNESS=$[$DELL_BRIGHTNESS*100/15]
	echo "New brightness: $NV_BRIGHTNESS"
	echo $NV_BRIGHTNESS > /sys/class/backlight/nv_backlight/brightness
done
