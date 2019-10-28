#!/usr/bin/env python3

"""
Walk through the GitHub repositories in repos.txt and pull metadata out of them for
later reuse.
"""

import collections
import io
import json
import re
import sys
import xml.dom.minidom as minidom

import yaml

from github_utils import get, collapse_list


class RepoSpider(object):
    def __init__(self, filename="repos.txt"):
        self.repos = []
        self.repo_data = {}
        self.group_data = collections.defaultdict(dict)
        self.populate_repo_list(filename)
        for (repo_id, branch_id) in self.repos:
            self.fetch_repo_data(repo_id, branch_id)
            self.check_repo_data(repo_id)
            self.fetch_repo_specs(repo_id)
            self.fetch_repo_revisions(repo_id)

    def populate_repo_list(self, filename):
        with io.open(filename) as fh:
            for line in fh:
                line = line.strip()
                if line[0] == "#":
                    continue
                words = line.split()
                repo_id = words.pop()
                branch_id = "master"
                if words:
                    branch_id = words.pop()
                self.repos.append([repo_id, branch_id])

    def fetch_repo_data(self, repo_id, branch_id):
        try:
            res = get(
                f"https://raw.githubusercontent.com/{repo_id}/{branch_id}/ietf.json"
            )
            self.repo_data[repo_id] = res.json()
        except (IOError, ValueError):
            return

    def check_repo_data(self, repo_id):
        group = self.repo_data[repo_id].get("group", None)
        if not group:
            sys.stderr.write(f"WARNING: Repo {repo_id} without group.\n")
            return
        if group not in self.group_data:
            self.group_data[group] = {"repos": []}

        repo_data = self.repo_data[repo_id]
        if repo_data.get("primary", False):
            if self.group_data[group]["repos"]:
                sys.stderr.write(
                    f"WARNING: Duplicate primary group {group} in {repo_id}.\n"
                )
            copy_data(
                repo_data,
                self.group_data[group],
                [
                    ("group_name", group),
                    ("group_type", None),
                    ("group_email", None),
                    ("group_chairs", []),
                    ("activity_exclude_labels": None)
                ],
                rm=True,
            )
        self.group_data[group]["repos"].append(repo_id)

    def fetch_repo_specs(self, repo_id):
        if self.repo_data[repo_id].get("repo_type", None) == "specs":
            if "spec_regex" in self.repo_data[repo_id]:
                matcher = re.compile(f"^{self.repo_data[repo_id]['spec_regex']}$")
            else:
                matcher = re.compile(
                    f"^draft-[^-]+-{self.repo_data[repo_id]['group']}-[^.]+\.(md|xml)$"
                )
            try:
                res = get(f"https://api.github.com/repos/{repo_id}/contents/")
                contents = res.json()
            except (IOError, ValueError):
                return

            files = {}
            for record in contents:
                if record["type"] != "file":
                    continue
                filename = record["name"]
                if matcher.match(filename):
                    file_url = record["download_url"]
                    try:
                        file_res = get(file_url)
                    except IOError:
                        return
                    filebase = filename.rsplit(".", 1)[0]
                    if filename.endswith(".md"):
                        files[filebase] = self.parse_md_rfc(file_res.text)
                    if filename.endswith(".xml"):
                        files[filebase] = self.parse_xml_rfc(file_res.text)
            self.repo_data[repo_id]["specs"] = files

    def fetch_repo_revisions(self, repo_id):
        if self.repo_data[repo_id].get("revisions_tagged", False):
            repo_tags = self.get_repo_tags(repo_id)
            for tag in repo_tags:
                try:
                    filename, revision = tag.rsplit("-", 1)
                except ValueError:
                    continue
                if filename in self.repo_data[repo_id]["specs"]:
                    revision = int(revision)
                    old_revision = self.repo_data[repo_id]["specs"][filename].get(
                        "revision", -1
                    )
                    if old_revision < revision:
                        self.repo_data[repo_id]["specs"][filename][
                            "revision"
                        ] = revision

    @staticmethod
    def parse_md_rfc(file_content):
        try:
            yaml_frontmatter = file_content.split("---", 2)[1]
            content = yaml.safe_load(yaml_frontmatter)
        except:
            return {"error": True}
        doc_data = {}
        copy_data(content, doc_data, [("title", None), ("github-issue-label", None)])
        return doc_data

    @staticmethod
    def parse_xml_rfc(file_content):
        try:
            dom = minidom.parseString(file_content)
        except:
            return {"error": True}
        pis = [
            node
            for node in dom.childNodes
            if node.nodeType == node.PROCESSING_INSTRUCTION_NODE
        ]
        try:
            issue_label = [
                node.data.strip() for node in pis if node.target == "github-issue-label"
            ][0]
        except IndexError:
            issue_label = None
        frontElement = dom.getElementsByTagName("front")[0]
        titleElement = frontElement.getElementsByTagName("title")[0]
        title = titleElement.firstChild.nodeValue
        return {"title": title, "github-issue-label": issue_label}

    @staticmethod
    def get_repo_tags(repo_id):
        tags = collapse_list(f"https://api.github.com/repos/{repo_id}/tags")
        return [i.get("name", None) for i in tags]

    def __str__(self):
        for group in self.group_data:
            self.group_data[group]["repos"] = {
                repo_id: self.repo_data[repo_id]
                for repo_id in self.group_data[group]["repos"]
            }
        return json.dumps(self.group_data, indent=2, sort_keys=True)


def copy_data(source, dest, targets, rm=False):
    for target in targets:
        assert isinstance(target, tuple)
        name = target[0]
        default = None
        if name in source:
            dest[name] = source[name]
            if rm:
                del source[name]
        else:
            dest[name] = target[1]


if __name__ == "__main__":
    print(RepoSpider())
