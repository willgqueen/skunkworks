import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import board  # noqa: E402

FIXTURE = ROOT / "tests/fixtures/workspace"


class NextActionTable(unittest.TestCase):
    """One case per row of docs/process.md#next-action, plus edge cases."""

    @classmethod
    def setUpClass(cls):
        items, cls.problems = board.collect(FIXTURE)
        cls.items = {i["id"]: i for i in items}

    def expect(self, item_id, action, waiting):
        item = self.items[item_id]
        self.assertEqual((item["next"], item["waiting_on"]), (action, waiting))

    def test_blocked(self):
        self.expect("001", "Resolve the block (tests fail), then resume", "you")

    def test_not_drafted(self):
        self.expect("002", "Run /define", "claude")

    def test_reopened(self):
        self.expect("003", "Revise define.md (/define)", "claude")

    def test_drafted_waits_on_user(self):
        self.expect("004", "Answer and approve the discover gate", "you")

    def test_approved_routes_by_size(self):
        self.expect("005", "Run /develop", "claude")

    def test_deliver_unauthorized(self):
        self.expect("006", "Run /deliver: plan, then one approval", "claude")

    def test_review_waits_for_merge(self):
        self.expect("007", "Merge, or resume /deliver", "you")

    def test_deliver_resume(self):
        self.expect("008", "Resume /deliver", "claude")

    def test_waived_counts_as_approved(self):
        self.expect("009", "Run /deliver", "claude")

    def test_waiting_on_you(self):
        self.expect("012", "AC3 pending (needs a GPU)", "you")

    def test_waiting_on_items(self):
        self.expect("013", "Wait for items 014, 015", "items")

    def test_deliver_waiver_ignored(self):
        self.expect("014", "Run /deliver: plan, then one approval", "claude")

    def test_revised_after_approval_stays_approved(self):
        self.expect("015", "Run /deliver", "claude")

    def test_unblocked_resumes(self):
        self.expect("018", "Resume /deliver", "claude")

    def test_merged_resumes_to_close(self):
        self.expect("019", "Resume /deliver", "claude")

    def test_revised_waits_on_user(self):
        self.expect("020", "Answer and approve the define gate", "you")

    def test_off_path_phase_routes_to_deliver(self):
        self.expect("022", "Run /deliver", "claude")

    def test_unfinished_dependency_waits(self):
        self.expect("032", "Wait for items 031", "items")

    def test_done_dependency_is_met(self):
        self.expect("033", "Run /define", "claude")

    def test_children_nested_with_progress(self):
        order = [i["id"] for i in board.collect(FIXTURE)[0]]
        self.assertEqual(order[order.index("030"):order.index("030") + 5], ["030", "031", "036", "032", "033"])
        self.assertEqual(self.items["036"]["depth"], 2)
        self.assertEqual(self.items["037"]["depth"], 0)
        self.assertTrue(self.items["030"]["next"].endswith("children: 1/4"))
        self.assertEqual(self.items["031"]["depth"], 1)

    def test_archived_dependency_is_met(self):
        self.expect("035", "Run /define", "claude")

    def test_failed_review_asks_to_fix(self):
        self.expect("038", "Fix the findings (/deliver), or accept them", "you")

    def test_render_and_json_fields(self):
        items, problems = board.collect(FIXTURE)
        self.assertIn("| ↳ ↳ 036 |", board.render(items, problems, 0, []))
        self.assertEqual((self.items["032"]["parent"], self.items["032"]["depends_on"]), ("030", ["031"]))

    def test_titles_keep_hash(self):
        self.assertEqual(self.items["016"]["title"], "Add C# bindings")
        self.assertEqual(self.items["017"]["title"], "Fix crash in #42")

    def test_done_hidden_and_unreadable_reported(self):
        self.assertNotIn("010", self.items)
        self.assertNotIn("021", self.items)
        self.assertEqual(len(self.problems), 1)

    def test_order_within_project(self):
        groups = [i["group"] for i in board.collect(FIXTURE)[0] if i["depth"] == 0]
        self.assertEqual(groups, sorted(groups, key=board.ORDER.get))


if __name__ == "__main__":
    unittest.main()
