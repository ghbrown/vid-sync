#!/bin/bash
docker build -t vid_sync .
docker run -v $(pwd):/vid_sync -t vid_sync python3 /vid_sync/app.py
