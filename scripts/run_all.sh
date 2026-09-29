#!/usr/bin/env bash
# run_all.sh - Run full simulation battery, analysis, and plotting
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "=========================================================="
echo "Running NS-3 TCP/UDP Congestion Analysis Pipeline"
echo "=========================================================="

cd "$ROOT_DIR"
python3 python/run_experiments.py
python3 python/plot_graphs.py

echo "=========================================================="
echo "All tasks complete! Results saved in results/ and graphs/."
echo "=========================================================="
