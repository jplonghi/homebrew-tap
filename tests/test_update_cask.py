import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location(
    'updater', Path(__file__).resolve().parents[1] / 'scripts/update-cask.py'
)
updater = importlib.util.module_from_spec(spec)
spec.loader.exec_module(updater)


class UpdateCaskTests(unittest.TestCase):
    def check_release(self, app, *, tag='v1.1.0', draft=False, prerelease=False,
                      missing_asset=False, bad_checksum=False, duplicate_checksum=False,
                      expected_error=False, old_digest=None):
        repository, asset = updater.APPS[app]
        payload = b'synthetic disk image'
        digest = hashlib.sha256(payload).hexdigest()
        release = {
            'tag_name': tag, 'draft': draft, 'prerelease': prerelease,
            'assets': [] if missing_asset else [{'name': asset}, {'name': 'SHA256SUMS.txt'}],
        }
        checksum = 'f' * 64 if bad_checksum else digest
        manifest = f'{checksum}  {asset}\n'
        if duplicate_checksum:
            manifest += manifest
        responses = [json.dumps(release).encode(), manifest.encode(), payload]
        original = f'  version "1.0.0"\n  sha256 "{old_digest or "0" * 64}"\n'
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'Casks').mkdir()
            cask = root / 'Casks' / f'{app}.rb'
            cask.write_text(original)
            other = root / 'Casks' / 'unrelated.rb'
            other.write_text('must remain unchanged')
            with patch.object(updater, 'ROOT', root), patch.object(updater, 'read_url', side_effect=responses) as read:
                if expected_error:
                    with self.assertRaises(ValueError):
                        updater.main(app)
                    self.assertEqual(cask.read_text(), original)
                else:
                    updater.main(app)
                    self.assertIn(f'version "{tag[1:]}"', cask.read_text())
                    self.assertIn(digest, cask.read_text())
                    self.assertEqual(read.call_args_list[0].args[0], f'https://api.github.com/repos/{repository}/releases/latest')
                    self.assertEqual(read.call_args_list[-1].args[0], f'https://github.com/{repository}/releases/download/{tag}/{asset}')
                self.assertEqual(other.read_text(), 'must remain unchanged')

    def test_verified_updates_for_each_app(self):
        for app in updater.APPS:
            with self.subTest(app=app):
                self.check_release(app)

    def test_rejected_releases_preserve_each_cask(self):
        cases = [
            {'draft': True}, {'prerelease': True}, {'tag': 'v1.1.0-beta'},
            {'tag': 'v0.9.0'}, {'tag': 'v1.0.0'}, {'missing_asset': True},
            {'bad_checksum': True}, {'duplicate_checksum': True},
        ]
        for app in updater.APPS:
            for case in cases:
                with self.subTest(app=app, case=case):
                    self.check_release(app, expected_error=True, **case)

    def test_unchanged_release_is_accepted(self):
        digest = hashlib.sha256(b'synthetic disk image').hexdigest()
        for app in updater.APPS:
            with self.subTest(app=app):
                self.check_release(app, tag='v1.0.0', old_digest=digest)


if __name__ == '__main__':
    unittest.main()
