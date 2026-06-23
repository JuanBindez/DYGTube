#!/bin/bash

set -e

VERSION=8
MINOR=0
PATCH=0
EXTRAVERSION=""
COMMIT="(New DYGTube v8)

Assisted-by: Gemini:Flash 3.5 [Google]
"
BRANCH="main"

if [[ -z $PATCH ]]; then
    PATCH=""
else
    PATCH=".$PATCH"
fi

if [[ $EXTRAVERSION == *"-rc"* ]]; then
    FULL_VERSION="$VERSION.$MINOR$PATCH$EXTRAVERSION"
else

    if [[ -z $EXTRAVERSION ]]; then
        FULL_VERSION="$VERSION.$MINOR$PATCH"
    else
        FULL_VERSION="$VERSION.$MINOR$PATCH.$EXTRAVERSION"
    fi
fi

git add .
git commit -s -m "$FULL_VERSION $COMMIT"
git push -u origin $BRANCH
git tag v$FULL_VERSION
git push --tags

echo "Build $FULL_VERSION completed successfully!"