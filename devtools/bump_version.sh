#!/usr/bin/env sh
# --------------------------------------------------------------------------- #
# Script to bump the version of RAMSTK after every commit.  The intent is to  #
# create a version number compliant with the SemVer 2.0 specification.        #
#                                                                             #
# Versioning scheme is:                                                       #
#                                                                             #
# If branch is master, version is M.m.p                                       #
# If branch is develop, version is M.m.p+SHA                                  #
# If branch is release, version is M.m.p-rc<BUILD>                            #
#                                                                             #
# where M = Major version                                                     #
#       m = minor version                                                     #
#       p = patch version                                                     #
#     SHA = short SHA-1 of commit                                             #
# <BUILD> = build number of release branch                                    #
#                                                                             #
# Major version number is manually bumped.                                    #
# minor version number is bumped whenever commit message begins with feat.    #
# patch version number is bumped whenever commit message begins with refactor #
# or fix.                                                                     #
# --------------------------------------------------------------------------- #

# Get the current version from setup.py and remove the single quotes.
cur_version=$(grep -m1 "__version__" $PWD/setup.py | cut -d '=' -f2)
cur_version=${cur_version//\'}

# Get the lastest RAMSTK tag and the latest commit's SHA-1.
last_tag="$(git tag -l | tail -n1)"
last_sha="$(git rev-parse --short HEAD)"

# Breakdown the version information.
strarr=(${cur_version//./ })
ver_major=${strarr[0]}
ver_minor=${strarr[1]}
ver_patch=${strarr[2]}

# Get the working branch.
this_branch="$(git branch | grep \* | cut -d ' ' -f2)"

# Get the number of commits made to this branch and increment by one for this
# commit's tag.
this_build=$(git rev-list --no-merges --count HEAD ^develop)
let this_build++

# Now trim the branch name to give us one of the following:
#
# master (gets tagged)
# develop (gets tagged)
# release (gets tagged)
# feature (does NOT get tagged)
# fix, hotfix (does NOT get tagged)
this_branch=${this_branch:0:7}

# Get the type of the current commit.  It will be one of:
#
# feat - new feature (minor version bump)
# fix - a bug fix (patch version bump)
# docs - documentation only change (no version bump)
# style - white-space, formatting, etc. (no version bump)
# refactor - improves maintainability, complexity, etc. (patch version bump)
# perf - improves performance (patch version bump)
# test - add or correct test (no version bump)
# chore - administrative task (no version bump)
this_commit="$(git log -1 --no-merges --pretty=%s | cat)"

# See if this commit warrants a patch or minor version bump.  Major version
# bumps will be done manually.
if [[ "$this_commit" =~ ^feat* ]];
then
    let ver_minor++
    ver_patch=0
fi
if [[ "$this_commit" =~ ^refactor* ]];
then
    let ver_patch++
fi
if [[ "$this_commit" =~ ^fix* ]];
then
    let ver_patch++
fi
if [[ "$this_commit" =~ ^perf* ]];
then
    let ver_patch++
fi

# Create the new version and tag following our rules.
new_version=$ver_major"."$ver_minor"."$ver_patch
new_tag=${last_tag//v}
if [[ "x$this_branch" == "xmaster" ]];
then
    new_tag=$new_version
elif [[ "x$this_branch" == "xdevelop" ]];
then
    new_tag=$new_version"+"$last_sha
elif [[ "x$this_branch" == "xrelease" ]];
then
    new_tag=$new_version"-rc"$this_build
fi

# Now update setup.py with the new version number if it differs from the
# current version.
if [ $new_version != $cur_version ];
then
    sed -i "s/^\(__version__\s*=\s*\).*$/\1'$new_version'/" $PWD/setup.py
    sed -i "s/^\(version\s*=\s*\).*$/\1'$new_version'/" $PWD/setup.cfg
fi

# Now tag the branch with the new tag.  Only master, develop, and release
# branches get tagged.
if [ ${new_tag} != ${last_tag//v} ];
then
    echo "Run this command git tag -s v${new_tag} -m 'Set tag v${new_tag}'"
fi
