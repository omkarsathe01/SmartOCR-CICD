#!/bin/bash
/usr/local/bin/gunicorn --chdir /work/Blue-Bricks-OCR -w 3 --pid process.pid --bind 0.0.0.0:5000 --daemon wsgi:application --access-logfile logs/access.log --error-logfile logs/error.log --timeout 500
echo "Service Started!"
