from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "recall_jsonl_corpus.py"
SPEC = importlib.util.spec_from_file_location("recall_jsonl_corpus", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class RecallTests(unittest.TestCase):
    def test_terms_preserve_phrase_and_remove_duplicates(self) -> None:
        self.assertEqual(
            MODULE.terms_from_query('"solid electrolyte" kinetics KINETICS'),
            ["solid electrolyte", "kinetics"],
        )

    def test_element_symbols_do_not_match_inside_words(self) -> None:
        record = {
            "id": "synthetic-1",
            "title": "Solid-state sodium battery with improved performance",
        }
        self.assertIsNone(MODULE.match_record(record, ["Li"], "all"))
        self.assertIsNone(MODULE.match_record(record, ["V"], "all"))

    def test_element_symbols_match_valid_formula(self) -> None:
        record = {
            "id": "synthetic-2",
            "title": "A synthetic LiFePO4, LiF, and V2O5 comparison",
        }
        self.assertIsNotNone(MODULE.match_record(record, ["Li", "V"], "all"))
        self.assertIsNotNone(MODULE.match_record(record, ["F"], "all"))

    def test_ordinary_terms_use_token_boundaries(self) -> None:
        record = {"id": "synthetic-3", "title": "Fictional operation study"}
        self.assertIsNone(MODULE.match_record(record, ["ion"], "all"))

    def test_text_is_not_double_counted_when_pages_exist(self) -> None:
        record = {
            "id": "synthetic-4",
            "title": "Kinetics",
            "text": "kinetics kinetics kinetics",
            "pages": [{"page": 1, "text": "kinetics"}],
        }
        labels = [label for label, _, _ in MODULE.searchable_parts(record)]
        self.assertNotIn("text", labels)
        self.assertIn("page 1", labels)

    def test_schema_rejects_non_string_required_fields(self) -> None:
        for invalid in (None, 7, True, ["value"]):
            with self.subTest(invalid=invalid):
                with self.assertRaises(SystemExit):
                    MODULE.validate_record({"id": invalid, "title": "title"}, 1)

    def test_source_redaction_covers_paths_and_file_uri(self) -> None:
        probes = [
            "/" + "Users" + "/example/private/file.pdf",
            "C:" + "\\" + "Users" + "\\" + "example" + "\\" + "file.pdf",
            "\\" + "\\" + "server" + "\\" + "share" + "\\" + "file.pdf",
            "file:" + "///" + "Users" + "/example/private/file.pdf",
            "relative/private/file.pdf",
        ]
        for probe in probes:
            with self.subTest(probe=probe):
                self.assertEqual(MODULE.safe_source(probe, False), "[source hidden]")

    def test_http_source_drops_query_and_fragment(self) -> None:
        result = MODULE.safe_source("https://example.org/paper?token=value#part", False)
        self.assertEqual(result, "https://example.org/paper")

    def test_malformed_url_port_is_hidden(self) -> None:
        self.assertEqual(
            MODULE.safe_source("https://example.org:not-a-port/paper", False),
            "[source hidden]",
        )

    def test_cli_hides_corpus_and_source_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            corpus = Path(temporary) / "library.jsonl"
            source = "/" + "Users" + "/example/private/source.pdf"
            corpus.write_text(
                json.dumps(
                    {
                        "id": "synthetic-cli",
                        "title": "Synthetic LiFePO4 kinetics",
                        "abstract": "A fictional record for a software test.",
                        "source": source,
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            environment = dict(os.environ)
            environment["PYTHONDONTWRITEBYTECODE"] = "1"
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--corpus",
                    str(corpus),
                    "--query",
                    "Li",
                ],
                capture_output=True,
                text=True,
                env=environment,
                check=True,
            )
            self.assertIn("[source hidden]", result.stdout)
            self.assertIn("untrusted evidence", result.stdout)
            self.assertNotIn(str(corpus), result.stdout)
            self.assertNotIn(source, result.stdout)


if __name__ == "__main__":
    unittest.main()
