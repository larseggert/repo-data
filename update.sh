#!/bin/bash


# Check to see if repo_data has changed.
git status --short repo_data.json | grep -s "M" || exit 0

# setup
git config user.email mnot@mnot.net
git config user.name mnot-bot
git remote set-url --push origin https://mnot:$GITHUB_TOKEN@github.com/ietf-github-services/repo-data
git checkout -B main origin/master

# Push the changes.
git add repo_data.json
git commit -m "update repo_data.json"
git push origin main
