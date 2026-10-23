cask "daylight" do
  version "2.6.4"
  sha256 "b564fd625de8760bcd656b7e195cfd3f7dcc0e064447b81d0cb0dda2bfa42c55"

  url "https://github.com/jplonghi/Daylight/releases/download/v#{version}/Daylight-macOS-universal.dmg"
  name "Daylight"
  desc "Desktop countdowns and focus timers"
  homepage "https://github.com/jplonghi/Daylight"

  livecheck do
    url :url
    strategy :github_latest
  end

  depends_on macos: :sonoma

  app "Daylight.app"

  caveats <<~EOS
    Quit Daylight before upgrading. This release is not notarized by Apple.
    If macOS blocks the first launch, follow Apple's Open Anyway instructions:
      https://support.apple.com/en-us/102445
  EOS
end
