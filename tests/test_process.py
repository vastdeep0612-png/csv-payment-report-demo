import unittest
from pathlib import Path

import process


ROOT = Path(__file__).resolve().parents[1]


class ReportTests(unittest.TestCase):
    def setUp(self):
        self.result = process.build_report(process.read_csv(ROOT / "sample.csv"))

    def test_known_total(self):
        self.assertEqual(self.result["total"], "22.75")

    def test_paid_rows(self):
        self.assertEqual(
            [row["order_id"] for row in self.result["paid"]],
            ["A-100", "A-101", "A-104"],
        )

    def test_refund_is_excluded(self):
        self.assertEqual(self.result["skipped"][0]["order_id"], "A-102")
        self.assertNotIn("A-102", [row["order_id"] for row in self.result["paid"]])

    def test_invalid_and_duplicate_rows(self):
        reasons = {row["order_id"]: row["reason"] for row in self.result["errors"]}
        self.assertEqual(reasons["A-103"], "not_a_number")
        self.assertEqual(reasons["A-100"], "duplicate_order_id")
        self.assertEqual(reasons["A-105"], "empty_amount")
        self.assertEqual(reasons["A-106"], "currency_symbol")
        self.assertEqual(reasons["A-107"], "date_invalid")
        self.assertEqual(reasons["A-108"], "empty_date")

    def test_written_output_matches(self):
        process.write_outputs(self.result, ROOT)
        output = (ROOT / "sample_output.csv").read_text(encoding="utf-8")
        self.assertIn("TOTAL,22.75", output)
        report = (ROOT / "sample_report.txt").read_text(encoding="utf-8")
        self.assertIn("valid_payments_total: 22.75", report)


if __name__ == "__main__":
    unittest.main()
