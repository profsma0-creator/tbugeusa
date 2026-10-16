#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# bootstrap.sh — prepare the toolchain for building the book
#
#   * installs Python deps (reportlab, matplotlib, pillow, fonttools)
#   * downloads OFL-licensed book fonts from the google/fonts repository
#   * instantiates static weights from the variable font masters
#
# Requires: python3, pip, gh (authenticated).  Idempotent — safe to re-run.
# ---------------------------------------------------------------------------
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FONTS="$ROOT/assets/fonts"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "==> book root: $ROOT"
mkdir -p "$FONTS"

# --- 1. Python dependencies -------------------------------------------------
echo "==> installing python dependencies"
python3 -m pip install --break-system-packages -q \
    reportlab matplotlib pillow fonttools 2>&1 | tail -3 || true

python3 - <<'PY'
import reportlab, matplotlib, PIL
print(f"    reportlab {reportlab.Version} | matplotlib {matplotlib.__version__} | pillow {PIL.__version__}")
try:
    import fontTools; print(f"    fonttools {fontTools.version}")
except ImportError:
    print("    fonttools MISSING (needed only to regenerate fonts)")
PY

# --- 2. Font masters --------------------------------------------------------
raw () {  # raw <repo-path> <outfile>
    gh api -H "Accept: application/vnd.github.raw" "/repos/google/fonts/contents/$1" > "$2"
    test -s "$2" || { echo "!! failed to fetch $1"; exit 1; }
}

if [ ! -f "$FONTS/OFL.txt" ]; then
    echo "==> downloading font masters (google/fonts)"
    raw "ofl/ebgaramond/OFL.txt"                        "$FONTS/OFL-EBGaramond.txt"
    raw "ofl/cinzel/OFL.txt"                            "$FONTS/OFL-Cinzel.txt"
    raw "ofl/lato/OFL.txt"                              "$FONTS/OFL-Lato.txt"
    raw "ofl/ebgaramond/EBGaramond%5Bwght%5D.ttf"       "$TMP/EBGaramond-VF.ttf"
    raw "ofl/ebgaramond/EBGaramond-Italic%5Bwght%5D.ttf" "$TMP/EBGaramond-Italic-VF.ttf"
    raw "ofl/cinzel/Cinzel%5Bwght%5D.ttf"               "$TMP/Cinzel-VF.ttf"
    for f in Regular Bold Italic Black Medium; do
        raw "ofl/lato/Lato-$f.ttf" "$FONTS/Lato-$f.ttf"
    done
fi

# keep the licence files together for print/compliance
[ -f "$FONTS/OFL.txt" ] || printf 'Licence files: OFL-EBGaramond.txt, OFL-Cinzel.txt, OFL-Lato.txt\n' > "$FONTS/OFL.txt"

# --- 3. Static instances ----------------------------------------------------
make_instance () {  # make_instance <master> <axis-spec> <out>
    if [ -f "$3" ]; then return 0; fi
    python3 -m fontTools.varLib.instancer -q "$1" "$2" -o "$3" >/dev/null 2>&1 \
        || { echo "!! failed instancing $2 from $1"; return 1; }
    echo "    + $(basename "$3")"
}

if [ -f "$TMP/EBGaramond-VF.ttf" ]; then
    echo "==> instantiating static weights"
    make_instance "$TMP/EBGaramond-VF.ttf"        "wght=400" "$FONTS/EBGaramond-Regular.ttf"
    make_instance "$TMP/EBGaramond-VF.ttf"        "wght=600" "$FONTS/EBGaramond-SemiBold.ttf"
    make_instance "$TMP/EBGaramond-VF.ttf"        "wght=700" "$FONTS/EBGaramond-Bold.ttf"
    make_instance "$TMP/EBGaramond-Italic-VF.ttf" "wght=400" "$FONTS/EBGaramond-Italic.ttf"
    make_instance "$TMP/EBGaramond-Italic-VF.ttf" "wght=600" "$FONTS/EBGaramond-SemiBoldItalic.ttf"
    make_instance "$TMP/Cinzel-VF.ttf"            "wght=400" "$FONTS/Cinzel-Regular.ttf"
    make_instance "$TMP/Cinzel-VF.ttf"            "wght=600" "$FONTS/Cinzel-SemiBold.ttf"
    make_instance "$TMP/Cinzel-VF.ttf"            "wght=700" "$FONTS/Cinzel-Bold.ttf"
    make_instance "$TMP/Cinzel-VF.ttf"            "wght=800" "$FONTS/Cinzel-ExtraBold.ttf"
fi

echo "==> fonts ready:"
ls -1s "$FONTS" | sed 's/^/    /'
echo "==> bootstrap complete"
