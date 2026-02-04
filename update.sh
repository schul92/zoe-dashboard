#!/bin/bash
source /home/ubuntu/.openclaw/workspace/dashboard/.venv/bin/activate
python3 /home/ubuntu/.openclaw/workspace/dashboard/aws-diagram-auto.py >> /home/ubuntu/.openclaw/workspace/dashboard/update.log 2>&1
