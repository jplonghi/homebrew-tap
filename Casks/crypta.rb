# frozen_string_literal: true

cask "crypta" do
  version "0.5.0"
  sha256 "b384c65a24913ee297c4b30f96197c8d2f20c9892f035dda7b0e743ebfb826c2"

  url "https://github.com/jplonghi/Crypta/releases/download/v#{version}/Crypta-macOS-arm64.dmg"
  name "Crypta"
  desc "Local encrypted vault for credentials and secure notes"
  homepage "https://github.com/jplonghi/Crypta"

  livecheck do
    url :url
    strategy :github_latest
  end

  depends_on arch: :arm64
  depends_on macos: :sonoma

  app "Crypta.app"

  caveats <<~EOS
    Crypta is a personal POC without an independent security audit.
    Use synthetic data while evaluating it. Quit Crypta before upgrading;
    development updates may require recreating older test vaults.
    This release is not notarized by Apple. If macOS blocks the first launch,
    follow Apple's Open Anyway instructions:
      https://support.apple.com/en-us/102445
  EOS
end
