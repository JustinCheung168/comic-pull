#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Put your pull commands here:
./pull.py superman-smashes-the-klan-2019
./pull.py supergirl-woman-of-tomorrow-2021
./pull.py absolute-batman-2024 --first-issue 8