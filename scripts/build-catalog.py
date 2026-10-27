#!/usr/bin/env python3
"""Checks every components/<id>/manifest.json and writes catalog.json, the one file OverPass reads.

Run from the repository root: python3 scripts/build-catalog.py [--check]
--check fails instead of writing when catalog.json is out of date (for CI).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KINDS = {"wine", "dlls", "wine-addons", "tool", "store", "import"}
ARCHES = {"arm64", "x86_64", "any"}
FEATURE = re.compile(r"^[a-z0-9-]+(>=[0-9]+)?$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")


def fail(where, message):
    sys.exit(f"{where}: {message}")


def check(folder, m):
    where = f"components/{folder}/manifest.json"
    for key in ("id", "name", "plainName", "summary", "kind", "install", "parts"):
        if key not in m:
            fail(where, f"missing '{key}'")
    if m["id"] != folder:
        fail(where, f"id '{m['id']}' differs from its folder")
    if m["kind"] not in KINDS:
        fail(where, f"unknown kind '{m['kind']}'")
    if "location" not in m["install"]:
        fail(where, "install has no location")
    for feature in m.get("requires", {}).get("wineFeatures", []):
        if not FEATURE.match(feature):
            fail(where, f"bad feature '{feature}' (name or name>=version)")
    if not m["parts"]:
        fail(where, "no parts")
    for part in m["parts"]:
        for key in ("name", "version", "authors", "licence", "upstream", "assets"):
            if key not in part:
                fail(where, f"part '{part.get('name', '?')}' is missing '{key}'")
        for asset in part["assets"]:
            if asset.get("arch") not in ARCHES:
                fail(where, f"{part['name']}: bad arch '{asset.get('arch')}'")
            if "url" in asset and not SHA256.match(asset.get("sha256", "")):
                fail(where, f"{part['name']}: a pinned url needs a sha256")
            if "url" not in asset and "urlTemplate" not in asset:
                fail(where, f"{part['name']}: asset has neither url nor urlTemplate")


def main():
    components = []
    for path in sorted((ROOT / "components").glob("*/manifest.json")):
        manifest = json.loads(path.read_text())
        check(path.parent.name, manifest)
        components.append(manifest)
    catalog = json.dumps({"format": 1, "components": components}, indent=2, ensure_ascii=False) + "\n"
    out = ROOT / "catalog.json"
    if "--check" in sys.argv:
        if not out.exists() or out.read_text() != catalog:
            sys.exit("catalog.json is out of date: run scripts/build-catalog.py")
        return
    out.write_text(catalog)
    print(f"catalog.json: {len(components)} components")


if __name__ == "__main__":
    main()
