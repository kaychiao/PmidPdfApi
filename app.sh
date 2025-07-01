#!/usr/bin/env bash

# Kill any existing process using port 8091
ps xf | grep '8091' | grep -v 'grep' | awk '{print "kill "$1}' | sh

# Set environment variables
export PMID_PDF_API_ENV_CONFIG='local'
export PYTHONPATH=$PYTHONPATH:`pwd`
export MYSQL_HOST='localhost'
export MYSQL_PORT=3306
export MYSQL_USER='root'
export MYSQL_PASSWORD='password'
export MYSQL_DB='pmid_pdf_db'
export PDF_ROOT_PATH='/Users/jiaoyk/Downloads/articles'

# Run the application with gunicorn
gunicorn "app:create_app()" --bind 0.0.0.0:8091 -w 4 --reload --timeout 300 --log-level=debug