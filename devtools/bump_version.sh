#!/usr/bin/env sh
# --------------------------------------------------------------------------- #
# Script to bump the version of RAMSTK after every commit.  The intent is to
# create a version number compliant with the SemVer 2.0 specification.
#
# Name branches as follows:
#     * fix/issue_###
#     * feature/issue_###
#     * working/issue_###
#     * release/vM.m.p
#
# If branch name begins with fix, bump patch version by one in VERSION.
# If branch name begins with feature, bump minor version by one in VERSION.
#
# - After merging a fix, tag master branch with tag vM.m.p where M.m.p is the
#   value in VERSION.
# - After merging a feature, tag master branch with tag vM.m.p+SHA where M.m.p
#   is the value in VERSION and SHA is the short SHA-1 value for the commit.
# - After creating a release branch, tag release branch with tag vM.m.p-rc1,
#   where M.m.p is the value in VERSION.
# - After merging a release, tag master branch with tag vM.m.p where M.m.p is
#   the value in VERSION.
# - After merging a working (any other) branch, tag master branch with tag
#   vM.m.p+SHA where M.m.p is the value in VERSION and SHA is the short SHA-1
#   value for the commit.
# --------------------------------------------------------------------------- #

# Get the current version from setup.py and remove the single quotes.
cur_version=$(cat $PWD/VERSION)
cur_version=${cur_version//\'}

# Breakdown the version information.
strarr=(${cur_version//./ })
ver_major=${strarr[0]}
ver_minor=${strarr[1]}
ver_patch=${strarr[2]}

# Get the lastest RAMSTK tag and the latest commit's SHA-1.
last_tag="$(git tag -l | tail -n1)"
last_sha="$(git rev-parse --short HEAD)"

# Get the number of commits made to this branch and increment by one for this
# commit's tag.
this_build=$(git rev-list --no-merges --count HEAD ^develop)
let this_build++

# Get the working branch and what the branch entails.
this_branch="$(git branch | grep \* | cut -d ' ' -f2)"
this_action=${this_branch:0:7}

DO_BUMP=0
DO_TAG=0
while [ $# -gt 0 ];
do
    case "$1" in
        -b | --bump)
            DO_BUMP=1
            ;;
        -t | --tag)
            DO_TAG=1
            ;;
    esac
    shift
done

if [ "x$this_action" = "xfix" ];
then
    let ver_patch++
    new_version=$ver_major"."$ver_minor"."$ver_patch
    new_tag="v"$new_version
elif [ "x$this_action" = "xfeature" ];
then
    let ver_minor++
    ver_patch=0
    new_version=$ver_major"."$ver_minor"."$ver_patch
    new_tag="v"$new_version
elif [ "x$this_action" = "xrelease" ];
then
    new_version=$ver_major"."$ver_minor"."$ver_patch"-rc"$this_build
    new_tag="v"$new_version
else
    new_version=$ver_major"."$ver_minor"."$ver_patch"+"$last_sha
    new_tag="v"$new_version
fi

if [ "x$DO_BUMP" = "x1" ];
then
    $(bump2version --current-version ${cur_version} --new-version ${new_version} patch $PWD/VERSION)
fi

if [ "x$DO_TAG" = "x1" ];
then
    git tag -s ${new_tag} -m 'Set tag ${new_tag}'
fi

exit 0
