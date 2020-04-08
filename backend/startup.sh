#!/bin/bash

set -m

python JobDispatcher.py &

flask run --host 0.0.0.0

fg %1