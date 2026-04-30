#!/usr/bin/env python3
"""Validates instrument TOML files for the teasel registry."""

import sys
import tomllib
import urllib.request
import urllib.error
from pathlib import Path

REQUIRED_FIELDS = ["slug", "name", "manufacturer", "type"]
ERRORS = []


def err(path: str, msg: str) -> None:
    ERRORS.append(f"{path}: {msg}")
    print(f"  ERROR: {msg}", file=sys.stderr)


def check_url(url: str, label: str, path: str) -> None:
    try:
        req = urllib.request.Request(url, method="HEAD")
        req.add_header("User-Agent", "teasel-validator/1.0")
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status == 404:
                err(path, f"{label} URL not found (404): {url}")
    except urllib.error.HTTPError as e:
        # 403/405 often means CDN blocks HEAD but URL is valid; only fail on 404
        if e.code == 404:
            err(path, f"{label} URL not found (404): {url}")
    except Exception as e:
        err(path, f"{label} URL unreachable ({e}): {url}")


def check_package(pkg: dict, path: str) -> None:
    distribution = pkg.get("distribution", "pypi")
    name = pkg.get("package", "")

    if distribution == "pypi":
        url = f"https://pypi.org/pypi/{name}/json"
    elif distribution == "npm":
        url = f"https://registry.npmjs.org/{name}"
    elif distribution == "cargo":
        url = f"https://crates.io/api/v1/crates/{name}"
    else:
        return  # unknown distribution, skip

    try:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", "teasel-validator/1.0")
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status != 200:
                err(path, f"package '{name}' not found on {distribution} (status {resp.status})")
    except urllib.error.HTTPError as e:
        err(path, f"package '{name}' not found on {distribution} (HTTP {e.code})")
    except Exception as e:
        err(path, f"could not verify package '{name}' on {distribution}: {e}")


def validate(toml_path: Path) -> None:
    path = str(toml_path)
    print(f"Validating {path}")

    try:
        with open(toml_path, "rb") as f:
            data = tomllib.load(f)
    except tomllib.TOMLDecodeError as e:
        err(path, f"invalid TOML: {e}")
        return

    instrument = data.get("instrument", {})

    for field in REQUIRED_FIELDS:
        if not instrument.get(field):
            err(path, f"missing required field: instrument.{field}")

    slug = instrument.get("slug", "")
    if slug and toml_path.stem != slug:
        err(path, f"slug '{slug}' does not match filename '{toml_path.stem}'")

    packages = data.get("mcp", {}).get("packages", [])
    if not packages:
        err(path, "must have at least one [[mcp.packages]] entry")

    for pkg in packages:
        check_package(pkg, path)
        if url := pkg.get("url"):
            check_url(url, "package url", path)

    if manual := instrument.get("manual"):
        check_url(manual, "manual", path)

    if image := instrument.get("image"):
        check_url(image, "image", path)

    for i, step in enumerate(data.get("setup", {}).get("steps", [])):
        if img := step.get("image"):
            check_url(img, f"setup step {i} image", path)


def main() -> None:
    args = sys.argv[1:]
    if not args:
        paths = list(Path("instruments").glob("*.toml"))
    else:
        paths = [Path(p) for p in args]

    if not paths:
        print("No TOML files found.")
        sys.exit(0)

    for path in paths:
        validate(path)

    if ERRORS:
        print(f"\n{len(ERRORS)} error(s) found:", file=sys.stderr)
        for e in ERRORS:
            print(f"  {e}", file=sys.stderr)
        sys.exit(1)
    else:
        print(f"\nAll {len(paths)} file(s) valid.")


if __name__ == "__main__":
    main()
