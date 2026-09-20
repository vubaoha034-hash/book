import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "dialogue_blocker", ROOT / "scripts/check_dialogue_adjacency.py"
)
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)

PHASE390_FAIL = """
“刘叔。”

“又怎么了？”

“你还欠我五文。”

“记账。”

“你每次都这么说。”

“那说明我没赖账。”
"""

PHASE393_FAIL = """
“这个就是顾承岳？”

顾承岳看向他。

小泥鳅下意识退了半步。

刘还山道：“你不是出来替那几个小的买早饭？”

“是啊。”

“那还不走？”

“他们饿一会儿又饿不死。”

刘还山伸手就在他脑袋上拍了一下。

“少学这些话。”
"""

PHASE363_POSITIVE = """
“你回来干什么。”

楚十三没接这句话。他把只剩四支箭的箭囊摘下来，直接塞进刘还山手里，自己探身出去。

“高处两个，右边门洞还有一个。”

刘还山已经把两支直的抽出来夹在指间。楚十三一伸手，他递过去一支；楚十三射完，手再往后一探，第二支已经到了掌心。

门洞里的人刚退，车底忽然传来木头崩裂的声音。

有人从另一侧把铁钩挂上了后轮。

刘还山转身压剑，楚十三没有跟着去砍铁钩。他先跨上车辕，把背后冲来的那个人逼退，随后弯腰抓住车栏。

刘还山肩头的旧伤被猛地扯开，手臂一软。

楚十三立刻换到了他这一侧。

“别过来。”

楚十三已经把肩膀抵进车栏和石墩之间。
"""


class DialogueAdjacencyBlockerTests(unittest.TestCase):
    def test_phase390_known_failure_blocks(self):
        result = MOD.analyze_text(PHASE390_FAIL)
        self.assertEqual(result["verdict"], "BLOCK")
        self.assertTrue(
            any("RAPID_SHORT_TURN_LADDER" in r["reasons"] for r in result["blocked_runs"])
        )

    def test_phase393_known_failure_blocks(self):
        result = MOD.analyze_text(PHASE393_FAIL)
        self.assertEqual(result["verdict"], "BLOCK")
        reasons = {reason for r in result["blocked_runs"] for reason in r["reasons"]}
        self.assertIn("QUESTION_ANSWER_LADDER", reasons)
        self.assertIn("ALTERNATING_QA_CHAIN", reasons)

    def test_phase363_positive_excerpt_not_structurally_blocked(self):
        result = MOD.analyze_text(PHASE363_POSITIVE)
        self.assertEqual(result["verdict"], "CLEAR")


if __name__ == "__main__":
    unittest.main()
