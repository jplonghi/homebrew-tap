# Daylight Homebrew tap

Install [Daylight](https://github.com/jplonghi/Daylight), desktop countdowns and focus timers for macOS 14 Sonoma or later. The universal app supports Apple silicon and Intel.

```sh
brew install --cask jplonghi/tap/daylight
```

If you already installed Daylight by dragging it into Applications, quit it and remove only the old `Daylight.app` before installing with Homebrew. Your countdowns remain in `~/Library/Application Support/Daylight/`.

Daylight is not yet notarized by Apple. If macOS blocks the first launch, follow [Apple's Open Anyway instructions](https://support.apple.com/en-us/102445). Homebrew does not remove this first-launch requirement.

## Update

Quit Daylight, then run:

```sh
brew update
brew upgrade --cask jplonghi/tap/daylight
```

## Uninstall

Disable Launch at login in Daylight and quit the app, then run:

```sh
brew uninstall --cask jplonghi/tap/daylight
```

Uninstalling preserves your saved countdowns. This cask deliberately has no `zap` rule that deletes personal data.

## Maintenance

The update workflow checks the latest public stable Daylight release every six hours. It can also be run manually from GitHub Actions. Scheduled runs may be delayed; GitHub can disable schedules in inactive public repositories, so check Actions if updates stop.

The updater downloads the version-specific DMG and checksum manifest, verifies their SHA-256 match, and commits the new version and checksum. It ignores draft and prerelease builds, rejects downgrades, and refuses changed assets for an existing version. It uses this repository's built-in Actions token; no cross-repository secret is needed.

To update locally, run `python3 scripts/update-cask.py`, review the diff, and commit it. After enabling Apple notarization upstream, remove the first-launch caveat from the cask and documentation.
