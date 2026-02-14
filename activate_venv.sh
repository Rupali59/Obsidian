#!/bin/zsh
# Zsh-compatible virtual environment activation script
# Usage: source activate_venv.sh

# Unalias deactivate if it exists (fixes zsh compatibility issue)
unalias deactivate 2>/dev/null

# Activate the virtual environment
source "$(dirname "$0")/.venv/bin/activate"
