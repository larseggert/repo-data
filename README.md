# IETF Repository Data Service

This repository gathers metadata from Github repositories for IETF-related work in the `repo_data.json` file.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Adding Your Repository to the Index](#adding-your-repository-to-the-index)
  - [The `ietf.json` File](#the-ietfjson-file)
  - [Specification Markup](#specification-markup)
  - [The `repos.txt` File](#the-repostxt-file)
- [Using `repo_data.json`](#using-repo_datajson)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


## Adding Your Repository to the Index

To have your repository included in the `repo_data.json` file:

1. Create an `ietf.json` file in the repo root. If it's the first one for your group, make sure you include the `group_info` object (see below).
2. Submit a pull request to update `repos.txt` in this repository.

Your repository's data should be reflected when the PR is merged. Subsequent updates to `ietf.json` and repo metadata should be reflected within six hours.


### The `ietf.json` File

The `ietf.json` file is a [JSON](https://tools.ietf.org/html/rfc8259) format with a top-level object. Its possible keys are:

- `group`: the short name of the [WG](https://datatracker.ietf.org/wg/) or [RG](https://datatracker.ietf.org/rg/) that owns this repo; e.g., `httpbis`, `intarea`.
- `repo_type`: one of `specs`, `tests`, `docs`, `website`, `registry`, `other`.
- `report_to`: list of addresses (see below);  Where weekly reports of issue and PR activity are sent. Optional.
- `issue_summary_to`: list of addresses (see below); Where weekly reports of open issues are sent. Optional.

Fields ending in `_to` are lists of e-mail addresses; special case `group_email` sends to the group e-mail address.

### Additional Field for `specs` Repos

Repos of type `specs` can have these additional fields:

- `revisions_tagged`: boolean indicating whether the repo followed the `filename-revision` tagging convention (as the [I-D-template](https://github.com/martinthomson/i-d-template) does). Defaults to False.
- `spec_regex`: a regular expression that matches specification files in the root directory. Optional; if omitted, files that match `draft-[^-]+-{group}-[^.]+\.(md|xml)` will be considered specifications.

### The `group_info` Object

Exactly one repo for each group can contain the `group_info` object, whose members are:

- `name`: the "full" name of the group.
- `type`: one of "wg", "rg", or "other".
- `email`: e-mail address for the group's mailing list. Optional.
- `chairs`: list of github usernames.
- `activity_exclude_labels`: list of strings that indicate Github issue labels (e.g., "editorial") that are filtered out of activity reports. Optional.


### Specification Markup

Additional metadata is gathered from specification documents in your repo. 

The following fields can be added in the YAML frontmatter of Markdown documents, or as a Processing Instruction (e.g., `<?github-issue-label foo?>`) in XML documents:

- `github-issue-label`: A GitHub issues label that is used to classify issues for this specification.


## The `repos.txt` File

This file is a simple, line-delimited list of repositories to monitor. Each line is the name of the owner and repository separated by a `/`. Optionally, this can be followed by a branch identifier after a space; the default is `master`.



## Using `repo_data.json`

If your application uses this data, please consider adding it to the [consumers list](https://github.com/ietf-github-services/repo-data/wiki/Consumers), so we can stay in touch.

