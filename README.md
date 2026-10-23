# Homebrew tap

Install [Daylight](https://github.com/jplonghi/Daylight), desktop countdowns and focus timers for macOS 14 Sonoma or later. The universal app supports Apple silicon and Intel.

```sh
brew install --cask jplonghi/tap/daylight
```

If you already installed Daylight by dragging it into Applications, quit it and remove only the old `Daylight.app` before installing with Homebrew. Your countdowns remain in `~/Library/Application Support/Daylight/`.

Daylight is not yet notarized by Apple. If macOS blocks the first launch, follow [Apple's Open Anyway instructions](https://support.apple.com/en-us/102445). Homebrew does not remove this first-launch requirement.

## Crypta

[Crypta](https://github.com/jplonghi/Crypta) is a local encrypted vault for credentials and secure notes. Requires an Apple Silicon Mac running macOS 14 Sonoma or later.

```sh
brew install --cask jplonghi/tap/crypta
```

Crypta is a personal POC without an independent security audit. Use synthetic data while evaluating it. It is ad-hoc signed and not notarized; Apple's first-launch instructions above also apply to Crypta.

If Crypta is already in Applications, quit it and remove only the old `Crypta.app` before installing with Homebrew. Keep your `.crypta` vault files. To update, quit Crypta, run `brew update`, then `brew upgrade --cask jplonghi/tap/crypta`. Back up your vault first; development updates may require recreating older test vaults.

To uninstall, quit Crypta and run `brew uninstall --cask jplonghi/tap/crypta`. This preserves your vault files and app preferences; the cask has no `zap` rule.

## Update Daylight

Quit Daylight, then run:

```sh
brew update
brew upgrade --cask jplonghi/tap/daylight
```

## Uninstall Daylight

Disable Launch at login in Daylight and quit the app, then run:

```sh
brew uninstall --cask jplonghi/tap/daylight
```

Uninstalling preserves your saved countdowns. This cask deliberately has no `zap` rule that deletes personal data.

## Maintenance

The update workflow checks the latest public stable release of each app every six hours. It can also be run manually from GitHub Actions. Scheduled runs may be delayed; GitHub can disable schedules in inactive public repositories, so check Actions if updates stop.

The updater downloads the version-specific DMG and checksum manifest, verifies their SHA-256 match, and commits the new version and checksum. It selects public stable releases, rejects draft and prerelease builds, rejects downgrades, and refuses changed assets for an existing version. It uses this repository's built-in Actions token; no cross-repository secret is needed.

To update locally, run `python3 scripts/update-cask.py daylight` or `python3 scripts/update-cask.py crypta`, review the diff, and commit it. After enabling Apple notarization upstream, remove the first-launch caveat from the cask and documentation.
