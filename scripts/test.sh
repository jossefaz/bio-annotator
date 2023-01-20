#!/usr/bin/env bash

set -e
set -x

# Check README.md is up to date
coverage run -m pytest tests ${@}