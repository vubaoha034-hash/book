# AGENTS.md

For any new chat or task continuation, start at `START_HERE.md` and run its current-state check before using historical phase instructions.

## Locked current novel mainline

For this project's current work, read `MAINLINE.md` and the task referenced by `state/project_state.json`. They define the single active improvement route. Preserve the original story and evidence; do not revive a historical phase or change the locked method without a recorded failed frozen test or an explicit scoped user change. Writer-only isolated contexts read their declared packet only; the coordinator settles state before and after that isolated run. The current mainline amends unfinished execution scope, not historical receipts or accepted research checkpoints.

检查点199：刘先生明确要求连续完成直到实际人工审核，常规中间环节不再询问授权。已完成唯一390字新开头与不同上下文的AI编辑、匿名AI读者及事实审查，原报告/证据/状态已保存。实际Sol / Max经运行核对；主写1、内部修订0，新稿真人UNKNOWN。接续[当前结果](docs/NOVEL_AUTONOMOUS_REVIEWED_OPENING_TO_HUMAN_RESULT_20261003.md)及[执行方式](modules/autonomous-to-human-review.md)，交付这份正文后收实际阅读反馈；AI赞成不晋级质量门。旧稿、197字保护、旧额度0、方法4、故事目标、既有真人FAIL和404未知保持。读取不重跑，不继续生成或扩到完整场景/V5。

检查点200：390字实际真人文笔/AI味与续读FAIL已另存。沿用连续执行授权，一次独立语言诊断后只调整当前输入呈现，冻结唯一375字新稿，另三个独立AI审核与证据结算完成。实际Sol / Max核对；新稿真人UNKNOWN，旧任务原件不改，旧保护/额度及方法4保持。见[当前结果](docs/NOVEL_OPENING_PROSE_REPAIR_RESULT_20261003.md)，下一步只交正文收实际阅读；常规中间不问授权，不循环求赞成或扩到V5。

检查点201：375字实际留存/悬念FAIL与AI味相对改善已记录。已在同一冻结事实内完成一次新短稿及独立编辑、匿名AI读者和事实审核；新稿真人UNKNOWN。见[当前结果](docs/NOVEL_OPENING_HOOK_TRIAL_RESULT_20261003.md)。只交这一份正文收实际阅读，旧稿/锁/额度/方法4保持；常规中间不问授权，不循环求赞成或扩到V5。

检查点202：401字已有刘先生“这个稍微好了一些。确实。”的相对正向反馈，见[原话](state/review_receipts/NOVEL_HOOK_TRIAL_401_HUMAN_PARTIAL_FEEDBACK_20261003.json)。续读与人物互动仍未明确，质量UNKNOWN；只收同一版本的阅读判断，不改稿、不调用模型或自动晋级。

检查点203：同一401字有少量续读意愿、互动更自然，见[真人原话](state/review_receipts/NOVEL_HOOK_TRIAL_401_HUMAN_WEAK_CONTINUATION_20261003.json)。只认可该短段两项目标，保留低强度限定；完整场景/TEST-01与迁移仍未通过。下一步按既有授权准备同场唯一300—500字接续，不改开头、旧稿/锁/额度或主线。

## Highest-priority execution-surface routing

Current scoped override (2026-10-03): task
`NOVEL-CODEX-REVIEW-INTEGRATION-AND-R2-DIAGNOSIS-20261003-01` explicitly authorizes
Codex coordination and independent review sessions. Follow
`docs/NOVEL_CODEX_REVIEW_INTEGRATION_20261003.md` and the live checkpoint. Prefer
GPT-6.1 Sol / Max, verified from actual runtime settings. Only the coordinator
writes business state; reviewers receive their assigned packet only, with no
tools, repository access, inherited chat, or other reports. This supersedes the
old browser transport for this round, without retrying its blocked task or
claiming an old callback. Cold screening failed its limited calibration and
cannot certify literary quality or the user's taste. This override supplies no
new prose budget, no V5, and no release of the old 197-character protection.

Historical checkpoint196 continuation: after the completed reentry/fact preparation, the user approved its concrete proposal and required direct completion. One fresh writer generated the only 395-character new opening short; a different fresh context returned FACT_CLEAR, with evidence settled by the coordinator. Read `docs/NOVEL_R2_REENTRY_ONE_SHORT_TRIAL_RESULT_20261003.md` and its native authorization/task/result. The single new budget is spent. New-version opening organization was authorized; old artifacts, locks, exhausted RC3 budget and human rejections remain intact. Next: actual human reading of this frozen short. No automatic A2, full scene, TEST-02, V5 or new life facts. FACT_CLEAR cannot become a human PASS.

历史检查点197：395字稿实际真人FAIL已另存，前一检查点的UNKNOWN仅为历史快照。已按用户要求主动学习专业资料并完成一次独立已知失败后的情绪/互动诊断。读取 [学习与适用边界](docs/NOVEL_EMOTION_PACING_PROFESSIONAL_STUDY_20261003.md)、[根因与原始证据](docs/NOVEL_EMOTION_REACTION_DIAGNOSIS_RESULT_20261003.md)及当前任务。复用 [人物反应与节奏](modules/emotion-reaction-and-pacing.md)作当前阶段参考，不把教程、失败标签和诊断塞入写作者上下文；未来只取三条简短正向原则。当前无新写作预算，不自动续写，旧锁和方法4保持。读取不重跑模型，原一次诊断已消费；未读完整视频/书籍，不宣称已学会或验证文风。


检查点198已按刘先生新要求接入两个实际独立AI角色：编辑读取必要事实和已知失败，匿名读者只看正文；原报告互不传递。实际Sol/Max已核对。编辑REVISE、AI读者YES与真人不想继续的FAIL不一致，不能晋级质量门。见[当前结果](docs/NOVEL_TWO_ROLE_OPENING_REVIEW_RESULT_20261003.md)及[调用方式](modules/two-role-opening-review.md)。取用固定提交的story-review/reader-sim，未安装整套规则。已推进一份既有姓名错位入口和冻结输入准备；当前预算零，后续写作者只读prepared_input.writer_packet。新版本开头重排须新的一次范围和预算，旧稿/197字保护和旧额度不变。读取不重跑，原评审各一次已消费。
This section selects the execution surface only. It does not override V3 content/phase routing, quality gates, or human gates. If an execution-route preference conflicts with a content or human gate, the gate wins.

- Default execution mode: `CHAT`.
- Every newly opened Chat execution uses `thinking_effort = EXTREME_HIGH`.
- CHAT covers story design/diagnosis/review/rewrite, ordinary web search and source reading, ordinary browser navigation/clicking, human-review-card preparation/handling, ordinary repository/connector reads, and small canonical writes that do not require a local runtime.
- Ordinary web or browser work does **not** imply Work.
- Use Work only when it is materially better: an unusually long autonomous workflow, many-step coordination across multiple apps/sites, Chat becoming materially slower/fragmented/unstable, or a genuinely Work-only capability.
- Use Codex local for local engineering: full repository access, shell/Python, tests, dependency installation, build/compilation, bulk file processing, or large-scale local Git.
- Execution routing never authorizes crossing a quality gate, phase gate, or human gate, and never supplies a required human verdict on the user's behalf.
- Reusable machine-readable policy: `rules/execution-routing-v1.json`.

## Repository purpose

This repository contains `novel-writing-master`, an evidence-driven Chinese-fiction Skill.

## Default version

Use V3 for new work. V2 files remain for backward compatibility.

Always read:

- `SKILL.md`
- `rules/pass-isolation.md`
- `workflows/07-novel-master-pipeline-v3.md` for full-production tasks

Load only the current phase files.

## Phase routing

### Source ingestion and story dissection

Use the existing V2 ingestion and dissection assets:

- `workflows/01-ingest-book.md`
- `workflows/05-deep-story-dissection.md`
- `scripts/ingest.py`

Extract abstract craft only. Do not publish protected source text or private personal samples.

### Story design and rewrite

Read:

- `modules/causal-proof-engine.md`
- `modules/emotion-payoff-ledger.md`
- `modules/hate-empathy-test.md`
- `modules/character-pressure-test.md`

Do not draft the full story until the story contract, causal chain, emotional debt, and character-choice evidence exist.

### Drafting

Use only the story contract, current causal row, current emotional-debt task, current character state, necessary rules, aesthetic baseline, previous ending, and next target.

Do not load all review modules during prose generation.

### Logic and continuity

Read:

- `modules/causal-proof-engine.md`
- `modules/developmental-editor.md` when the spine, structure, or pacing is in doubt
- `modules/continuity-editor.md`
- `rules/novel-logic-checklist.md`

Treat an unexplained simpler solution as a blocker when it can dissolve the core conflict without meaningful cost.

### Emotion, hate, empathy, and payoff

Read:

- `modules/emotion-payoff-ledger.md`
- `modules/hate-empathy-test.md`
- `rules/reader-reward-rhythm.md`

Do not count shock reactions, facial expressions, apologies, or narration as payoff unless power, relationship, choice, interest, or cost changes.

### Reader checks

Use `modules/opening-retention-reader.md` and `modules/beta-reader-panel.md`.

Call a review independent only when it actually runs in a fresh context or comes from an external reader. Otherwise label it a simulated reader lens.

### Line edit and de-AI

Read:

- `modules/aesthetic-fingerprint.md`
- `modules/line-editor-deslop.md`
- `rules/no-ai-smell.md`
- `rules/reader-trust-and-economy.md`

Run last. Change no plot facts. Handle at most five high-impact patterns per pass.

## Quality evidence

Use `config/novel-quality-gates.v3.json` and `templates/v3-evidence-packet-template.md`.

A gate requires located textual evidence. A checked box, self-score, role-played reader count, or existing file is not quality evidence.

## Review discipline

- Diagnose before rewriting.
- Logic before language.
- Causality before pacing cosmetics.
- Emotional debt before isolated “爽点”.
- Concrete choice before backstory explanation.
- Preserve effective awkwardness, subtext, and voice.
- After a change, recheck its downstream facts, knowledge, objects, rules, and relationships.

## Repository changes

1. Preserve the root `SKILL.md` entrypoint.
2. Keep V2 assets for compatibility unless a migration explicitly removes them.
3. Add specialized methods as modules, workflows, templates, or config.
4. Update `README.md` for user-facing changes.
5. Run `python scripts/validate_skill.py`.
6. Never commit private source books, complete copyrighted text, or personal style samples to this public repository.
