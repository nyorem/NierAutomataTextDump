#! /usr/bin/env bash

rm -rf website/missions
mkdir website/missions
scripts/organizeText.py

cd website

rm -rf .git
git init
git checkout -b gh-pages
git add -A
git commit -m "deploy"

# If we are not inside a GitHub action, do the following
if [ -z ${CI+x} ]; then
    git remote add origin git@github.com:nyorem/NierAutomataTextDump.git
    git push -f origin gh-pages
fi

cd -
