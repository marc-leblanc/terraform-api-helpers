![pre-commit](https://github.com/marc-leblanc/terraform-api-helpers/workflows/pre-commit/badge.svg)

# Terraform API Helper Scripts

This repo provides helper scripts to work with Terraform Cloud/Enterprise API.

## [Python](./python)

| Script | Description |
| --- | --- |
| set_var.py | Sets variables on a workspace using a CSV file |
| fetch_oauth.py | Fetches oauth information required to create workspaces |
| workspaces.py | Creates a Workspace, connects to a VCS repo, sets working directory. Can also list existing workspaces and related information. List runs on a workspace and status. |
| credential_copy.py | Can copy local environment variable credentials to a workspace. Supported **--gcp**, **--github_pat** |


## [Bash](./bash)

| Script | Description |
| --- | --- |
| set_var.sh | Sets variables on a workspace using a CSV file |
| fetch_oauth.sh | Fetches oauth information required to create workspaces |
| create_workspace.sh | Creates a Workspace, connects to a VCS repo and can set variables |