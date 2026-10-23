# frozen_string_literal: true

cask "crypta" do
  version "0.5.0"
  sha256 "772fff2153657fcbdebd6039d8b313fdb03b5e8e3c4921d773ac3c5d6a5c46d7"

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
