#!/bin/sh
aerich upgrade
uvicorn gptbase_enterprise.app:app --host 0.0.0.0 --port 8000  --workers 2 --reload