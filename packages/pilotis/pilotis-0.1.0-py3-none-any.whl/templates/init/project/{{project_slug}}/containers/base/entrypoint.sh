#!/bin/bash -eu

source "$(poetry env list --full-path | cut -d' ' -f1)/bin/activate"

exec "$@"