#!/bin/bash
set -x -e

DIST=$(mktemp -d /tmp/api-docs.XXXXXXXX)

GIT_REPO=$1

git clone $GIT_REPO $DIST
rm -rf $DIST/*
cp -r api/* $DIST

pushd $DIST
git add -A :/
git commit -a -m "Updated at $(date -R)" || true
git push origin +master
popd

rm -rf $DIST
