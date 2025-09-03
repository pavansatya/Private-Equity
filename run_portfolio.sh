#!/bin/zsh
echo "==== $(date) starting ===="

# Use Anaconda Python
PY="/opt/anaconda3/bin/python3"

# (optional) Make sure PATH includes Anaconda bin
export PATH="/opt/anaconda3/bin:/usr/local/bin:/usr/bin:/bin"

# If your script needs a specific conda env, see the "Using a conda env" section below.

cd "/Users/krishvenigalla/Desktop/Private Equity" || { echo "cd failed"; exit 1; }

echo "Using python: $($PY -V 2>&1)"
exec "$PY" -u "/Users/krishvenigalla/Desktop/Private Equity/portfolio_tracker.py"

