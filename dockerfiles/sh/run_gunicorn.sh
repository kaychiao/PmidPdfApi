#!/bin/bash

check_mysql() {
  export PYTHONPATH=$PYTHONPATH:`pwd`
  python3 initialization/check/check_main.py
  ret=$?
  if [ "$ret" != 0 ]; then
      echo "\033[31m MySQL validation failed, startup unsuccessful. \033[1m"
      exit 1
  fi
}

run_gunicorn() {
  local port=$1
  gunicorn "app:create_app()" --bind 0.0.0.0:$port --timeout 300 -w 4 --reload
}

__main() {
  local port=$1
  # Uncomment this if you implement MySQL check
  # check_mysql
  run_gunicorn $port
}

port="$1"

__main $port