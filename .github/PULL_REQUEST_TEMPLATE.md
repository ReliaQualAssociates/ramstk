## Pull Request Checklist

- Code Style
  - [ ] Code is following code style guidelines.
  - [ ] Followed in new code.
  - [ ] Corrected in existing code whenever possible.
  - [ ] Spelling and English grammar errors have been eliminated.
  - [ ] Attribute and variable names make sense.
  - [ ] Stub files created or updated.
  - [ ] New code is readable.
  - [ ] Execute 'make maintain' before committing changes and fix any issues.
  - [ ] Code is not overly complicated; refactor if it is.
  - [ ] Debugging, including print(), statements have been removed.

- Tests
  - [ ] At least one test for all newly created functions/methods?
  - [ ] Tests capture key use cases.
  - [ ] Enough edge cases covered for comfort.
  - [ ] Code coverage has not decreased.

- Documentation
  - [ ] Update api documentation to reflect the changes made.
  - [ ] Update the user documentation to reflect the changes made.

- Chores
  - [ ] Problem areas outside the scope of this PR have an # ISSUE: comment
 decorating the code block.  These # ISSUE: comments are automatically
  converted to issues on successful merge.  Alternatively, you can manually
   raise an issue for each problem area you identify.
  - [ ] TODO and FIXME statements have been have been converted to # ISSUE
 : comments or removed in their entirety.
  - [ ] \# ISSUE: comments have been removed for those issues this PR
   addresses.
  - [ ] Update the features section of README.md for newly added work stream modules.

- [ ] All PR checks pass.
  - [ ] Execute 'make format', 'make stylecheck', 'make typecheck', and 'make
   lint' before committing changes and fix any issues.
  - [ ] Failing static checks are only applicable to code outside the scope of
   this PR.

## Does this PR introduce a breaking change?
- [ ] Yes
- [ ] No

<!-- If yes, describe the impact and migration path below. -->

## Other information
<!-- Provide any other information that is import to this PR such as
screenshots if this impacts the GUI. -->
