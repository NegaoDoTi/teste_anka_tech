#!/bin/sh

python app.py &

python run.py &

wait -n

exit $?
