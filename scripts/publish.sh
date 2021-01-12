#! /usr/bin/env bash

scripts/organizeText.py

cd website

rm -rf .git
git init
git remote add origin git@github.com:nyorem/NierAutomataTextDump.git
git checkout -b gh-pages
git add -A
git commit -m "deploy"
git push -f origin gh-pages

cd -
