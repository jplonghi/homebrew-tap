#!/usr/bin/env python3
"""Pin the cask to the latest public stable release after verifying its DMG."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
APPS = {
    "daylight": ("jplonghi/Daylight", "Daylight-macOS-universal.dmg"),
    "crypta": ("jplonghi/Crypta", "Crypta-macOS-arm64.dmg"),
}


def read_url(url, *, api=False):
    headers = {"User-Agent": "jplonghi-homebrew-updater"}
    if api and os.environ.get("GH_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GH_TOKEN"]
    with urlopen(Request(url, headers=headers), timeout=120) as response:
        return response.read()


def main(app="daylight"):
    repository, asset_name = APPS[app]
    cask = ROOT / "Casks" / f"{app}.rb"
    release = json.loads(read_url(
        f"https://api.github.com/repos/{repository}/releases/latest", api=True
    ))
    tag = release["tag_name"]
    if release["draft"] or release["prerelease"] or not re.fullmatch(r"v\d+\.\d+\.\d+", tag):
        raise ValueError("Expected a published stable vMAJOR.MINOR.PATCH release")
    version = tag[1:]
    assets = {asset["name"] for asset in release["assets"]}
    if not {asset_name, "SHA256SUMS.txt"} <= assets:
        raise ValueError("Release must contain the DMG and SHA256SUMS.txt")
    base = f"https://github.com/{repository}/releases/download/{tag}"
    checksums = read_url(f"{base}/SHA256SUMS.txt").decode("utf-8")
    matches = re.findall(r"^([0-9a-f]{64})  " + re.escape(asset_name) + r"$", checksums, re.MULTILINE)
    if len(matches) != 1:
        raise ValueError("Expected exactly one DMG checksum")
    digest = hashlib.sha256(read_url(f"{base}/{asset_name}")).hexdigest()
    if digest != matches[0]:
        raise ValueError("Downloaded DMG does not match published checksum")

    source = cask.read_text()
    old_version = re.search(r'^  version "([0-9.]+)"$', source, re.MULTILINE).group(1)
    old_digest = re.search(r'^  sha256 "([0-9a-f]{64})"$', source, re.MULTILINE).group(1)
    if tuple(map(int, version.split("."))) < tuple(map(int, old_version.split("."))):
        raise ValueError("Refusing to downgrade the cask")
    if version == old_version and digest != old_digest:
        raise ValueError("Existing release changed; publish a new version instead")
    source = re.sub(r'^  version "[0-9.]+"$', f'  version "{version}"', source, count=1, flags=re.MULTILINE)
    source = re.sub(r'^  sha256 "[0-9a-f]{64}"$', f'  sha256 "{digest}"', source, count=1, flags=re.MULTILINE)
    cask.write_text(source)
    print(f"Verified {app} {version}: {digest}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("app", choices=APPS, nargs="?", default="daylight")
    main(parser.parse_args().app)
