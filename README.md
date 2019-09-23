# IETF Repository Data Service

This repository gathers metadata from Github repositories that have opted in. It is used to help provide a growing number of services to them.


## Adding Your Repository to the Index

To add your repository:

1. Create an `ietf.json` file in the root of your repository
2. Submit a pull request to update `repos.txt` in this repository

Your repository's data (and any subsequent updates) should be reflected when the PR is merged. Subsequent updates to `ietf.json` should be reflected within six hours.


### The `ietf.json` File

The `ietf.json` file is a [JSON](https://tools.ietf.org/html/rfc8259) format with a top-level object. Its possible keys are:

- `group`: the short name of the [WG](https://datatracker.ietf.org/wg/) or [RG](https://datatracker.ietf.org/rg/) that owns this repo; e.g., `httpbis`, `intarea`.
- `primary`: boolean indicating whether additional information is present; see below.
- `repo_type`: one of `specs`, `tests`, `docs`, `website`, `other`.
- `report_to`: list; currently can contain `group_email`. Where weekly reports of issue and PR activity are sent to. Optional.
- `report_exclude_labels`: list of strings that indicate Github issue labels that are filtered out of reports. Optional.

Repos of type `specs` can have these additional fields:

- `spec_regex`: a regular expression that matches specification files in the root directory; only valid on a `repo_type` of `specs`.
- `revisions_tagged`: boolean indicating whether the repo followed the `filename-revision` tagging convention. Defaults to False.

If `primary` is `true`, these additional fields can be present:

- `group_name`: the "full" name of the group.
- `group_type`: one of "wg" or "rg".
- `group_email`: e-mail address for the group's mailing list. Optional.
- `group_chairs`: list of github usernames.

Note that each group (identified by the `group` field) can have only one `primary` repo.


### Specification Markup

- `issue_label`: 


### The `repos.txt` File

This file is a simple, line-delimited list of repositories to monitor. Each line is the name of the owner and repository separated by a `/`. Optionally, this can be followed by a branch identifier after a space; the default is `master`.


