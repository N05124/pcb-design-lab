#!/usr/bin/env bash
# Download the Freerouting releases used by the benchmark into benchmark/tools/.
set -euo pipefail
DIR="$(cd "$(dirname "$0")/.." && pwd)/tools"
mkdir -p "$DIR"
for v in 2.5.0 2.1.0; do
  f="$DIR/freerouting-$v.jar"
  [ -s "$f" ] && { echo "have $f"; continue; }
  curl -fSL -o "$f" "https://github.com/freerouting/freerouting/releases/download/v$v/freerouting-$v.jar"
done
ls -la "$DIR"
