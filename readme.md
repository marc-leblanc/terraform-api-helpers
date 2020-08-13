![pre-commit](https://github.com/marc-leblanc/terraform-api-helpers/workflows/pre-commit/badge.svg)

# Terraform API Helper Scripts

This repo provides helper scripts to work with Terraform Cloud/Enterprise API.

## [Python](./python)

| Script | Description |
| --- | --- |
| set_var.py | Sets variables on a workspace using a CSV file |
| fetch_oauth.py | Fetches oauth information required to create workspaces |
| create_workspace.py | Creates a Workspace, connects to a VCS repo, sets working directory |
| credential_copy.py | Can copy GOOGLE_CREDENTIALS local environment variable to a workspace |


## [Bash](./bash)

| Script | Description |
| --- | --- |
| set_var.sh | Sets variables on a workspace using a CSV file |
| fetch_oauth.sh | Fetches oauth information required to create workspaces |
| create_workspace.sh | Creates a Workspace, connects to a VCS repo and can set variables |