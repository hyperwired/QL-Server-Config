#!/bin/bash
cd "$(dirname "$0")"
LD_LIBRARY_PATH="." exec ./qzeroded.x86 "$@"