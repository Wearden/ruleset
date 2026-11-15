"""Negative checks use in-memory mutations; no source files are changed."""
import copy
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from verify_sources import ROOT, verify


class SourceVerificationTests(unittest.TestCase):
    def setUp(self):
        self.lock = json.loads((ROOT / "sources.lock.json").read_text(encoding="utf-8"))

    def mutated(self, lock):
        original = Path.read_text
        def read(path, *args, **kwargs):
            if path == ROOT / "sources.lock.json":
                return json.dumps(lock)
            return original(path, *args, **kwargs)
        with patch.object(Path, "read_text", read):
            return verify()

    def test_locked_content_matches(self):
        self.assertEqual(verify(), [])

    def test_changed_hash_is_rejected(self):
        lock = copy.deepcopy(self.lock)
        lock["legacy"][0]["sha256"] = "0" * 64
        self.assertTrue(any("Hash mismatch" in e for e in self.mutated(lock)))

    def test_path_escape_is_rejected(self):
        lock = copy.deepcopy(self.lock)
        lock["legacy"][0]["path"] = "../outside-repository.yaml"
        self.assertTrue(any("escapes repository" in e for e in self.mutated(lock)))

    def test_unknown_mapping_is_rejected(self):
        lock = copy.deepcopy(self.lock)
        lock["mappings"][0]["source_paths"] = ["not-a-pinned-source.yml"]
        self.assertTrue(any("Unpinned source" in e for e in self.mutated(lock)))


if __name__ == "__main__":
    unittest.main()
