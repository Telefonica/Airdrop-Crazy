#!/bin/sh

/etc/init.d/tor start &
gunicorn -b 0.0.0.0:5000 app  --log-file '/var/log/aidrop-hack.log' --log-level=debug