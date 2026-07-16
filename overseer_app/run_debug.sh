#!/usr/bin/env bash
# run_debug.sh — Launch Overseer APP on Linux / macOS
set -e
cd "$(dirname "$0")"
echo "Starting Overseer APP (Debug Mode)..."
python3 main.py
