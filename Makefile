
PYTHON=python3

.PHONY: repo_data.json
repo_data.json: fresh repo_spider.py repos.txt
	$(PYTHON) repo_spider.py > repo_data.json

.PHONY: fresh
fresh:
	git pull origin master

.PHONY: update
update: repo_data.json
	git status --short repo_data.json | grep -s "M" || exit 0
	git add repo_data.json
	git commit -m "update repo_data.json"
	git push origin master
