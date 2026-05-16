#!/bin/bash
cd /Users/one/Projects/toolhunt-dev || exit 1
export DEEPSEEK_API_KEY='sk-73c23be4cbf548a7b9cc3783d2cd4691'
export https_proxy=http://127.0.0.1:7890
export http_proxy=http://127.0.0.1:7890
python3 scripts/generate-post.py 2>&1
