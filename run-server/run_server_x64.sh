#!/bin/bash
cd "$(dirname "$0")"
LD_LIBRARY_PATH="./linux64" exec ./qzeroded.x64 "$@"