#!/bin/bash

if [ -z "$1" ]
  then
    echo "Usage: rename_photos <photos_dir>"
    exit 1
fi

PHOTOS_DIR=$1

echo "Rename photos in dir $PHOTOS_DIR"
exiv2 -r'%Y-%m-%d_%H.%M.%S' -F rename $PHOTOS_DIR/*
