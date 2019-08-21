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

# Get the working branch and trim the branch name to give us one of the
# following:
#
# master (gets tagged)
# develop (gets tagged)
# release (gets tagged)
# fix (does NOT get tagged)
# feature (does NOT get tagged)
# refactor (does NOT get tagged)
# tests (does NOT get tagged)
# docs (does NOT get tagged)
# chore (does NOT get tagged)
this_branch="$(git branch | grep \* | cut -d ' ' -f2)"
this_action=${this_branch:0:7}

if [[ "$this_action" =~ ^fix* ]];
then
    let ver_patch++
    new_version=$ver_major"."$ver_minor"."$ver_patch
    new_tag="v"$new_version

    $(bump2version --current-version ${cur_version} --new-version ${new_version} patch $PWD/VERSION)

    echo "1. Create pull request to merge into master: ghpr -t 'Merge $this_branch into master' -h master -b $this_branch"
    echo "2. Once merged to master, create tag on master: git tag -s ${new_tag} -m 'Set tag ${new_tag}'"
    echo "3. Create pull request to merge into develop: ghpr -t 'Merge $this_branch into develop' -h develop -b $this_branch"
    echo "4. Once merged to master, create tag on develop: git tag -s ${new_tag} -m 'Set tag ${new_tag}'"
    echo "5. Push tags to remote: git push --tags"
    echo "6. Deploy to GitHub releases, pypi, and conda."
elif [[ "$this_action" =~ ^feat* ]];
then
    let ver_minor++
    ver_patch=0
    new_version=$ver_major"."$ver_minor"."$ver_patch
    new_tag="v"$new_version

    $(bump2version --current-version ${cur_version} --new-version ${new_version} minor $PWD/VERSION)

    echo "1. Create pull request to merge into develop: ghpr -t 'Merge $this_branch into develop' -h develop -b $this_branch"
    echo "2. Once merged to develop, create tag on develop: git tag -s ${new_tag} -m 'Set tag ${new_tag}'"
    echo "3. [Optional] Create release branch: git checkout -b release/${new_version}"
    echo "4. [Optional] Push release branch to remote: git push --set-upstream origin release/${new_version}"
elif [[ "$this_action" =~ ^relea* ]];
then
    new_version=$ver_major"."$ver_minor"."$ver_patch"-rc"$this_build
    new_tag="v"$new_version

    $(bump2version --current-version ${cur_version} --new-version ${new_version} ${level} $PWD/VERSION)

    echo "1. Create pull request to merge into master: ghpr -t 'Merge $this_branch into master' -h master -b $this_branch"
    echo "2. Once merged to master, create tag on master: git tag -s ${new_tag} -m 'Set tag ${new_tag}'"
    echo "3. Push tags to remote: git push --tags"
    echo "6. Deploy to GitHub releases, pypi, and conda."
elif [[ "$this_action" =~ ^devel* ]];
then
    new_version=$ver_major"."$ver_minor"."$ver_patch"+"$last_sha
    new_tag="v"$new_version

    $(bump2version --current-version ${cur_version} --new-version ${new_version} ${level} $PWD/VERSION)

    echo "1. Create tag on develop: git tag -s ${new_tag} -m 'Set tag ${new_tag}'"
    echo "2. Deploy to GitHub releases."
else
    echo "1. Create pull request to merge into develop: ghpr -t 'Merge $this_branch into develop' -h develop -b $this_branch"
    echo "2. Once merged, run this script again."
fi

exit 0
