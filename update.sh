#!/bin/bash

# setup
git config user.email mnot@mnot.net
git config user.name mnot-bot
git remote set-url --push origin https://mnot:$GITHUB_TOKEN@github.com/mnot/ietf-repo-data

# Update repo_data.json
python3 repo_spider.py > repo_data.json

# Check to see if repo_data has changed.
git status --short repo_data.json | grep -s "M" || exit 0

# Push the changes.
git add repo_data.json
git commit -m "update repo_data.json"
git push origin master