## Pull request checklist

The following checklist must be completed before a pull request will be merged.
With the exception of the first item, you may create the pull request before
all items are satisfied and work towards 100% compliance.
- [ ] Add link in this PR (below) to the issue or issues it is addressing.  If
  an issue doesn't currently exist, write one before this pull request.
- [ ] Ensure the driving issue(s) include a comment containing one or more
  requirement and/or coding standard.
- [ ] One or more tests (new or revised) associated with this PR to verify the
  requirements.
- [ ] Bump the patch level in VERSION file.
- [ ] New code is type checked; execute mypy against your code.
- [ ] Run linters (at minimum pycodestyle, pydocstyle, pylint) and address
  suggestions.  Not all suggestions need be 'fixed', but those that aren't
  should be discussed in the comments describing your rationale.
- [ ] All new functions/methods have a McCabe score <10.
- [ ] Entire test suite passes.
- [ ] Coveralls reported code coverage has not decreased.
- [ ] Better Code Hub compliance has not decreased.  If your functions/methods
  show up in one of the 10 categories, fix it.  You do not need to fix existing
  code, but try to if it's related to your contribution.

## Pull request type

<!-- Please do not submit update to dependencies unless it fixed an issue. -->

<!-- Try to limit you pull request to one type, submit multiple pull requests
is needed. -->

Check the type of change this PR introduces:
- [ ] Fix
- [ ] Feature
- [ ] Refactor (including code style change)
- [ ] Test
- [ ] Doc
- [ ] Chore

## Explain the problem this PR fixes
Issue Number(s): Addresses issue(s) #

## Does this PR introduce a breaking change?
- [ ] Yes
- [ ] No

<!-- If yes, describe the impact and migration path below. -->

## Other information
<!-- Provide any other information that is import to this PR such as
screenshots if this impacts the GUI. -->
