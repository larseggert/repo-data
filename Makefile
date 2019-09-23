
PYTHON=python3
MAKE=make

.PHONY: repo_data.json
repo_data.json: fresh repo_spider.py repos.txt
	$(PYTHON) repo_spider.py > repo_data.json

.PHONY: fresh
fresh:
	git pull origin master

.PHONY: update
update: repo_data.json
	$(MAKE) changed_data && $(MAKE) push

.PHONY: changed_data
changed_data:
	git status --short repo_data.json | grep -s "M" || exit 1

.PHONY: push
push:
	git add repo_data.json
	git commit -m "update repo_data.json"
	git push origin master
