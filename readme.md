# API Helper Scripts For Terraform Cloud/Enterprise

This repo contains scripts to help use the Terraform Cloud/Enterprise API.

**Scripts**

| Script | Description |
| --- | --- | --- |
| [create_workspace.sh](#creating-workspaces) | Create Terraform Cloud Workspaces |
| [set_vars.sh](#setting-variables)  | Set variables on a workspace |
| [fetch_oauth](#fetch-oauth) | Fetch Organization Oauth information |

**Set up**

To use these scripts, you need to set an environment variables for TFE_ADDRESS, TFE_API_TOKEN and TFE_ORGANIZATION

```
export TFE_ADDRESS=app.terraform.io
export TFE_ORGANIZATION=my_org_name
export TFE_API_TOKEN=***************************
```

## <a name="createws"></a>Creating Workspaces

The create workspace is able to:

* Create a basic workspace
* Create a workspace and attach a VCS Repository
* Set variables on the newly created workspace

Instructions for connecting to VCS
1. First you need to use the [fetch_oauth.sh](#fetchoauth) scripts to get the oauth token for the VCS
2. Get your repo in the form of **user/repo** or **organization/repo** . The VCS connection **must** have access to this repo.
3. Make note of the OAUTH token

Usage:
```
create_workspace -w {workspace_name} [-o {OAUTH_TOKEN} -r {repo} -f {variable_csv_file}]
```
| Option | Description | Required |
| --- | --- | --- |
| -w | Workspace Name | Yes |
| -o | OAUTH Token *(required if using VCS repo)| No |
| -r | Repo slug in the form of user/repo or organization repo | No |
| -f | Variable CSV File. See [set_vars instructions](#setvars) for setup | No

## <a name="setvars"></a>Setting Variables

**Usage**

`./set_vars.sh -w {workspace_name} -f {key_value_file}`


**CSV File Instructions**

In the form of
```
variable_name([a-z][A-Z][0-9]),value,sensitive(true|false),category(terraform|env),description(string)
```
Example:
```
foo,bar,true,terraform,sensitive terraform variable description
bar,foo,false,env,not sensivite  environment variable description
bard,food,false,env,not sensivite variable description
```

[Example File](kv_sample.txt)

## <a name=fetchoauth></a> Fetch Oauth

The fetch oauth script provides information for VCS connections. The only set up for this script is to set the TFE_ADDRESS, TFE_ORGANIZATION and TFE_API_TOKEN envrionment variables.

Usage:
```./fetch_oauth.sh```

## To Do (or not)
- Functions functions functions. Usage, payload_push....
- Checking if the variables already exist or not
- Add option to create new/update variables. This currently will error on variables that already exist
- Further data validation, empty lines etc.
