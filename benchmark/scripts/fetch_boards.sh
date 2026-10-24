#!/usr/bin/env bash
# Fetch every GitHub board in boards.json at the pinned ref (KiCad-7-readable
# revisions), checking out only the .kicad_pcb/.kicad_pro/.kicad_dru files.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p boards
python3 - <<'PY' | while IFS=$'\t' read -r repo ref dir file; do
import json
for b in json.load(open("boards.json"))["boards"]:
    if not b.get("repo"):
        continue
    parts = b["path"].split("/")          # boards/<dir>/<file...>
    print("\t".join([b["repo"], b.get("ref", "HEAD"), parts[1], "/".join(parts[2:])[:-len(".kicad_pcb")]]))
PY
  echo "== $dir @ $ref"
  [ -d "boards/$dir/.git" ] || git clone -q --filter=blob:none --no-checkout "$repo" "boards/$dir"
  (
    cd "boards/$dir"
    if [ "$ref" = "HEAD" ]; then git fetch -q --depth 1 origin; ref_to=FETCH_HEAD; else git fetch -q --depth 1 origin "$ref"; ref_to=FETCH_HEAD; fi
    for ext in kicad_pcb kicad_pro kicad_dru; do
      git checkout -q "$ref_to" -- "$file.$ext" 2>/dev/null || true
    done
    ls -la "$file".kicad_* 2>/dev/null | awk '{print "   ", $5, $9}'
  )
done
