# Contributing to cadCAD

:+1::tada: First off, thanks for taking the time to contribute! :tada::+1:

The following is a set of guidelines for contributing to cadCAD. 
Use your best judgment, and feel free to propose changes to this document in a pull request.

### Pull Requests:

Pull Request (PR) presented as "->".

General Template:

`user:branch -> org:staging`

Contributing a new feature:

`user:feature -> org:staging`

Contributing to an existing feature:

`user:feature -> org:feature`

### General Advise for Forked Repositories:
1. `git pull fork staging`
2. `git checkout -b feature` (new feature)
3. Apply your awesomeness! (Commit Often)
4. `git push fork feature`
5. Apply a rebase/merge strategy you're comfortable with (Recommended Below).
6. Submit PR from `user:staging` into `org:staging`
7. PR is queued for review
8. PR Reviewed (Update necessary if rejected)
9. PR Approved (There may be circumstances delaying the merge.)
10. Your contribution merged into next feature release on `org:master`

### Recommended Strategy: [Rebase](https://git-scm.com/book/en/v2/Git-Branching-Rebasing)
1. Add cadCAD-org/cadCAD as remote within you forked project locally.
2. `git checkout remote/master`
3. `git pull remote master`
4. `git checkout your_branch`
5. `git rebase master`
6. Resolve merge conflicts (while leveraging rebase commands)
7. `git push fork your_branch`

Thanks! :heart:
