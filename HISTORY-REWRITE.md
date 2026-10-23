# History rewrite (2026-10-23)

On October 23, 2026 this repository's history was rewritten to remove files
that recorded named university staff or contained real award records:
two feedback-meeting transcripts, four emails from research administrators,
and two real award documents with the workflow's output for each. They were
removed from `main` first (see `Feedback Meetings/README.md`) and then from
every commit.

- **Commits before August 13, 2026 are unchanged.** The 43 commits from
  August 13 onward have new SHAs.
- **`history/commit-map-2026-10-23.txt` maps each old commit SHA to its new one.**
  Use it to translate an old pin, such as `554f815` in an evaluation record.
- **The file contents of `main` are byte-identical** to `main` before the rewrite.
- **Pull requests and their discussion** remain in the private archive of the
  original repository, as do the original commits and the four closed issues.
- **The 18 open issues were recreated here as #1–#18.** GitHub doesn't transfer
  issues from a private repository to a public one. Each recreated issue and
  comment names its original author and date, and
  `history/issue-map-2026-10-23.txt` maps original issue numbers to new ones.

If you have a clone made before this date, delete it and clone again. Pushing
from an old clone would bring the removed history back.
