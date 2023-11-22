#!/bin/sh

SCRIPTS_DIR=$(dirname "$0")



python "$SCRIPTS_DIR/export.py" --platform=ios --arch=x86_64 --config=debug
python "$SCRIPTS_DIR/export.py" --platform=ios --arch=arm64-v8a --config=debug
python "$SCRIPTS_DIR/export.py" --platform=ios --arch=armeabi-v7a --config=debug



python "$SCRIPTS_DIR/export.py" --platform=ios --arch=x86_64 --config=release
python "$SCRIPTS_DIR/export.py" --platform=ios --arch=arm64-v8a --config=release
python "$SCRIPTS_DIR/export.py" --platform=ios --arch=armeabi-v7a --config=release
