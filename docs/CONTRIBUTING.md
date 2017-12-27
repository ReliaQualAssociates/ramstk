# Contributing to the Reliability ToolKit (RTK)

Thank you for taking the time to contribute!

The following is a set of guidelines for contributing to RTK, which is hosted in the [RTK repository](https://github.com/weibullguy/rtk) on GitHub. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

[How Can I Contribute?](#how-can-i-contribute)
  * [Reporting Bugs](#reporting-bugs)
  * [Suggesting Enhancements](#suggesting-enhancements)
  * [Pull Requests](#pull-requests)

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report for RTK. Following these guidelines helps maintainers and the community understand your report, reproduce the behavior, and find related reports.

> **Note:** If you find a **Closed** issue that seems like it is the same thing that you're experiencing, open a new issue and include a link to the original issue in the body of your new one.

#### Before Submitting a Bug Report

* **Perform a cursory search** to see if the problem has already been reported. If it has **and the issue is still open**, add a comment to the existing issue instead of opening a new one.

#### How to Submit a Good Bug Report

Bugs are tracked as [GitHub issues](https://guides.github.com/features/issues/).

Explain the problem and include additional details to help maintainers reproduce the problem:

* **Use a clear and descriptive title** for the issue to identify the problem.
* **Describe the exact steps which reproduce the problem** in as many details as possible; **don't just say what you did, but explain how you did it**. For example, if you moved the cursor to the end of a line, explain if you used the mouse, or a keyboard shortcut.
* **Provide specific examples to demonstrate the steps**. Include links to files or GitHub projects, or copy/pasteable snippets, which you use in those examples. If you're providing snippets in the issue, use [Markdown code blocks](https://help.github.com/articles/markdown-basics/#multiple-lines).
* **Describe the behavior you observed after following the steps** and point out what exactly is the problem with that behavior.
* **Explain which behavior you expected to see instead and why.**
* **Include screenshots and animated GIFs** which show you following the described steps and clearly demonstrate the problem.  You can use [this tool](https://www.cockos.com/licecap/) to record GIFs on macOS and Windows, and [this tool](https://github.com/colinkeenan/silentcast) or [this tool](https://github.com/GNOME/byzanz) on Linux.
* **If the problem wasn't triggered by a specific action**, describe what you were doing before the problem happened.

Include details about your configuration and environment:

* **Which version of RTK are you using?**
* **What's the name and version of the OS you're using**?

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for RTK, including completely new features and minor improvements to existing functionality. Following these guidelines helps maintainers and the community understand your suggestion and find related suggestions.

Before creating enhancement suggestions, please check [this list](#before-submitting-an-enhancement-suggestion) as you might find out that you don't need to create one. When you are creating an enhancement suggestion, please [include as many details as possible](#how-do-i-submit-a-good-enhancement-suggestion).

#### Before Submitting a Suggested Enhancement

* **Perform a cursory search** to see if the problem has already been reported. If it has **and the issue is still open**, add a comment to the existing issue instead of opening a new one.

#### How to Submit a Good Enhancement Suggestion

Enhancement suggestions are tracked as [GitHub issues](https://guides.github.com/features/issues/).

* **Use a clear and descriptive title** for the issue to identify the suggestion.
* **Provide a step-by-step description of the suggested enhancement** in as many details as possible.
* **Provide specific examples to demonstrate the steps**. Include copy/pasteable snippets which you use in those examples, as [Markdown code blocks](https://help.github.com/articles/markdown-basics/#multiple-lines).
* **Describe the current behavior** and **explain which behavior you expected to see instead** and why.
* **Include screenshots and animated GIFs** which help you demonstrate the steps or point out the part of RTK which the suggestion is related to. You can use [this tool](https://www.cockos.com/licecap/) to record GIFs on macOS and Windows, and [this tool](https://github.com/colinkeenan/silentcast) or [this tool](https://github.com/GNOME/byzanz) on Linux.
* **Explain why this enhancement would be useful** to most RTK users.

### Pull Requests

* Do not include issue numbers in the PR title.
* Include screenshots and animated GIFs in your pull request whenever possible.
* Document new code.
* End all files with a newline.
* Avoid platform-dependent code.

## Styleguides

### Git Commit Messages

* Use the present tense
* Use the imperative mood
* Limit the first line to 72 characters or less
* Reference pull requests and issues after the first line

### Guidelines

#### Never Commit Code That Doesn't Have a Test

And make sure the test(s) pass before committing.  If you add functionality of RTK, there should be one or more tests for the new functionality.  There should be a test to ensure the new code works with good inputs.

#### Never Commit Code That Doesn't Run

Run the code and correct all errors before committing. Make sure that newly added files are committed. If they are missing your local copy will run fine but nobody else will be able to run RTK.  This is not desirable.

#### Double check what you commit

Do a git pull --rebase to keep your checkout up-to-date. Invoke git diff before committing. Take messages from git about conflicts, unknown files, etc. seriously. git diff will tell you exactly what you will be committing. Check if that's really what you intended to commit.

#### Always add descriptive log messages

Log messages should be understandable to someone who sees only the log. They shouldn't depend on information outside the context of the commit. Try to put the log messages only to those files which are really affected by the change described in the log message.

In particular put all important information which can't be seen from the diff in the log message.

#### Don't Mix Formatting Changes with Code Changes

Changing formatting like indenting or white spaces blows up the diff, so that it is hard to find code changes if they are mixed with re-indenting commits or similar things when looking at the logs and diffs later. Committing formatting changes separately solves this problem.

#### Respect other developer's code

Respect the policies of application and library maintainers, and consult with them before making large changes.

Source control systems are not a substitute for developer communication.

#### Announce Changes in Advance

When you plan to make changes which affect a lot of different code in RTK's codebase, announce them in advance.  By announcing the changes in advance, developers are prepared, and can express concerns before something gets broken.

#### Code Review by Other Developers

Don't commit changes to the public API of RTK without prior review by other developers. Requiring a review for these changes is intended to avoid problems for the users of the APIs and to improve the quality of the APIs.

#### Take Responsibility for Your Commits

If your commit breaks something or has side effects on other code, take the responsibility to fix or help fix the problems.

#### Don't Commit Code You Don't Understand

Avoid things like "I don't know why it crashes, but when I do this, it does not crash anymore." or "I'm not completely sure if that's right, but at least it works for me.".

If you don't find a solution to a problem, discuss it with other developers.
Don't commit if other developers disagree

If there are disagreements over code changes, these should be resolved by discussing them, not by forcing code on others by simply committing the changes.

#### Backport Bug Fixes

If you commit bug fixes, consider porting the fixes to other branches. Use the same comment for both the original fix and the backport, that way it is easy to see which fixes have been backported already.

#### Use Issue System Numbers

If you fix bugs reported on the issue system, add the bug number to the log message. In order to keep the bug tracking system in sync with the git repositories, you should reference the bug report in your commits, and close the fixed bugs in the bug tracking system.

This doesn't mean that you don't need an understandable log message. It should be clear from the log message what has been changed without looking at the bug report.

#### Commit Complete Changesets

git has the ability to commit more than one file at a time. Therefore, please commit all related changes in multiple files, even if they span over multiple directories at the same time in the same commit. This way, you ensure that git stays in a runnable state before and after the commit and that the commit history is more helpful.

Commits should be preferably "atomic" - not splittable. That means that every bugfix, feature, refactoring or reformatting should go into an own commit. This, too, improves the readability of the history. Additionally, it makes porting changes between branches (cherry-picking) and finding faulty commits (by bisecting) simpler.

#### GUI Changes

If your commit causes user visible GUI changes, add the GUI keyword to the log message.
