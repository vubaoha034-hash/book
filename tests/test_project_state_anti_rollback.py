from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "validate_project_state_transition.py"
SPEC = importlib.util.spec_from_file_location("state_guard", MODULE_PATH)
assert SPEC and SPEC.loader
state_guard = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(state_guard)


class ProjectStateAntiRollbackTests(unittest.TestCase):
    def _state(self) -> dict:
        return {
            "accepted_checkpoint": {
                "phase_ordinal": 40,
                "progress_ordinal": 220,
            },
            "rollback": {"authorized": False, "receipt": None},
            "accepted_task_ids": ["BOOK-02-211-220"],
        }

    def test_lower_progress_is_rejected(self) -> None:
        verdict, _ = state_guard.validate_transition(
            self._state(),
            phase_ordinal=40,
            progress_ordinal=210,
            task_id=None,
            task_status=None,
            rollback_authorized=False,
        )
        self.assertEqual(verdict, state_guard.REGRESSION)

    def test_lower_phase_is_rejected(self) -> None:
        verdict, _ = state_guard.validate_transition(
            self._state(),
            phase_ordinal=20,
            progress_ordinal=999,
            task_id=None,
            task_status=None,
            rollback_authorized=False,
        )
        self.assertEqual(verdict, state_guard.REGRESSION)

    def test_missing_candidate_progress_is_unknown_not_not_started(self) -> None:
        verdict, _ = state_guard.validate_transition(
            self._state(),
            phase_ordinal=40,
            progress_ordinal=None,
            task_id=None,
            task_status=None,
            rollback_authorized=False,
        )
        self.assertEqual(verdict, state_guard.UNKNOWN)

    def test_forward_progress_passes(self) -> None:
        verdict, _ = state_guard.validate_transition(
            self._state(),
            phase_ordinal=40,
            progress_ordinal=230,
            task_id=None,
            task_status=None,
            rollback_authorized=False,
        )
        self.assertEqual(verdict, state_guard.PASS)

    def test_cli_rollback_flag_without_durable_receipt_cannot_bypass(self) -> None:
        verdict, _ = state_guard.validate_transition(
            self._state(),
            phase_ordinal=40,
            progress_ordinal=200,
            task_id=None,
            task_status=None,
            rollback_authorized=True,
        )
        self.assertEqual(verdict, state_guard.REGRESSION)

    def test_durable_authorized_rollback_can_pass(self) -> None:
        state = self._state()
        state["rollback"] = {
            "authorized": True,
            "receipt": {
                "rollback_authorized": True,
                "from_checkpoint": 220,
                "to_checkpoint": 200,
                "reason": "synthetic test",
            },
        }
        verdict, _ = state_guard.validate_transition(
            state,
            phase_ordinal=40,
            progress_ordinal=200,
            task_id=None,
            task_status=None,
            rollback_authorized=True,
        )
        self.assertEqual(verdict, state_guard.PASS)

    def test_accepted_task_cannot_be_redispatched(self) -> None:
        verdict, _ = state_guard.validate_transition(
            self._state(),
            phase_ordinal=40,
            progress_ordinal=220,
            task_id="BOOK-02-211-220",
            task_status="PENDING",
            rollback_authorized=False,
        )
        self.assertEqual(verdict, state_guard.REGRESSION)

    def test_accepted_task_replay_is_idempotent(self) -> None:
        verdict, _ = state_guard.validate_transition(
            self._state(),
            phase_ordinal=40,
            progress_ordinal=220,
            task_id="BOOK-02-211-220",
            task_status="ACCEPTED",
            rollback_authorized=False,
        )
        self.assertEqual(verdict, state_guard.PASS)


if __name__ == "__main__":
    unittest.main()
