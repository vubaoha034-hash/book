# STEP-01 Migration Audit

Audit date: 2026-08-12 (Asia/Hong_Kong)

## Source before migration

- Source exists: YES
- Source path: `C:\Users\Administrator\OneDrive\文档\ChatGPT\蒸馏小说`
- Git repository: YES
- Branch: `benchmark-v1`
- HEAD: `0b7f55df788f03facf22f831f650db3b753281fd`
- Remote: `origin https://github.com/vubaoha034-hash/book.git`
- Upstream: `origin/benchmark-v1`
- Upstream divergence: ahead 0 / behind 0
- Staged changes: 0
- Unstaged changes: 0
- Untracked files reported by normal status: 0
- Unpushed commits: 0
- Git refs: 8
- Commits reachable from all refs: 73
- Tags: 0
- `git fsck --no-dangling`: PASS

## Important local-only assets

`benchmark\_private` existed under the old project and was ignored by Git. It contained local corpus material, Style/Future Holdout partitions, prior run outputs, workspaces, cached upstream checkouts and local helper/configuration artifacts. Re-cloning GitHub would not have preserved these files.

- Actual regular files: 2190
- Total bytes: 36,008,044
- Source reparse points: 2 (`workspaces\oh-story-narrative\.agents\skills` and `workspaces\oh-story-style\.agents\skills`)

An earlier recursive display counted 2197 views because it traversed those directory links. The canonical copy inventory excludes link-expanded duplicates and contains 2190 regular files.

## Migration method

The migration was a non-destructive copy, not a move and not a clone:

1. Copied the repository, including `.git`, from C to `E:\蒸馏小说\repo` while excluding the physical `benchmark\_private` payload.
2. Copied the private Benchmark payload to `E:\蒸馏小说\_private\09_Benchmark`.
3. Added an ignored compatibility junction at `E:\蒸馏小说\repo\benchmark\_private` pointing to the external private payload.
4. Created external raw-source, structured-text, cache, temp and log directories.
5. Left the C source directory intact.

Robocopy used `/E /COPY:DAT /DCOPY:DAT /R:2 /W:1 /XJ`; it did not use `/MOVE`, `/MIR`, or deletion.

## Post-copy verification

- Source HEAD: `0b7f55df788f03facf22f831f650db3b753281fd`
- Target HEAD immediately after copy: `0b7f55df788f03facf22f831f650db3b753281fd`
- Source and target branch/upstream status immediately after copy: identical and clean
- Source refs: 8
- Target refs: 8
- Ref differences: 0
- Source commits: 73
- Target commits: 73
- Source `git fsck --no-dangling`: PASS
- Target `git fsck --no-dangling`: PASS
- Private source regular files: 2190
- Private target regular files: 2190
- Missing private files: 0
- Extra private files: 0
- SHA-256 mismatches: 0
- C source deleted: NO

## Data-preservation conclusion

Git history, tracked files, ignored Benchmark assets, local workspaces and holdout data were preserved. No uncommitted or unpushed Git work existed at migration start. The original C directory remains the rollback source until an external reviewer chooses otherwise.
