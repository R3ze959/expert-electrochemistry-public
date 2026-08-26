from __future__ import annotations

import json
import unittest
from pathlib import Path


CASES = Path(__file__).parents[1] / "evals" / "behavior-cases.json"


class BehaviorCaseSchemaTests(unittest.TestCase):
    def test_behavior_case_schema(self) -> None:
        payload = json.loads(CASES.read_text(encoding="utf-8"))
        self.assertEqual(payload["schema_version"], 1)
        cases = payload["cases"]
        self.assertGreaterEqual(len(cases), 8)
        identifiers = [case["id"] for case in cases]
        self.assertEqual(len(identifiers), len(set(identifiers)))
        for case in cases:
            self.assertIsInstance(case["prompt"], str)
            self.assertIsInstance(case["should_use_full_workflow"], bool)
            self.assertTrue(case["required_behaviors"])
            self.assertTrue(case["forbidden_behaviors"])


if __name__ == "__main__":
    unittest.main()
