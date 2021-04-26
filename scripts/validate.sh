#!/usr/bin/env sh
set -euo pipefail

pip install -r tests/requirements.txt --user

python -m autopep8 --exit-code --diff --recursive --max-line-length=100 share_prices tests
