"""Protect expanded IDs and mixed verification classes in the source-of-truth inventory."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from check_phase import requirement_classes  # noqa: E402 # Import local tool after its path is set.


class RequirementInventoryTests(unittest.TestCase):
    def test_ranges_and_multiple_ids_on_one_line(self) -> None:
        result = requirement_classes(
            "- `ADM-01..05 [A]` CRUD\n- `OPS-01 [A]` lifecycle; `OPS-02 [E]` selector"
        )
        self.assertEqual(len(result), 7)
        self.assertEqual(result["ADM-05"], ("AUTO",))
        self.assertEqual(result["OPS-01"], ("AUTO",))
        self.assertEqual(result["OPS-02"], ("EMU",))

    def test_device_evidence_is_retained_alongside_emulator(self) -> None:
        result = requirement_classes("- `TRK-06 [E]` simulation. `[D]` real GPS.")
        self.assertEqual(result["TRK-06"], ("EMU", "DEVICE"))


if __name__ == "__main__":
    unittest.main()
