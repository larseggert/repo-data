#!/bin/bash

# Check to see if repo_data has changed.
git status --short repo_data.json | grep -s "M" || exit 0

# Push the changes.
git add repo_data.json
git commit -m "update repo_data.json"
git push origin master