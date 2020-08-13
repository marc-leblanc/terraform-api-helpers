# Python Terraform Cloud API Helper Scripts

## Fetch OAuth Information

**fetch_oauth.py** retrieves OAuth information required to create a VCS backed Workspace. You will need to save the OAuth Token from the output

`fetch_oauth.py`

```
python fetch_oauth.py
🔧 Fetching VCS and oauth information ...
✅ Pulled VCS information for leblanchq creation completed...
VCS Connection Information
---------------
Name: GitHub - Personal
ID: oc-zasdasdasdJJJJJJJJ
Token ot-Yt5vw7NnNnNnNnNn
```

## Create Workspaces

**create_workspace.py** provides the ability to quickly create and configure a workspace in Terraform Cloud/Enterprise. Workspaces have the option of specifying the version of Terraform, attaching to a VCS Repository and setting a working directory.


```
usage: create_workspace.py [-h] --workspace WORKSPACE_NAME
                           [--tf-version TF_VERSION] [--repo REPO]
                           [--working-dir WORKING_DIR]
                           [--oauth-token OAUTH_TOKEN]
```


| Argument | Description | Required |
| --- | --- | --- |
| -w, --workspace | Workspace name | Yes |
| -t, --tf-version | Requested Terraform Version. Defaults to latest available on Terraform Cloud/Enterprise | No |
| -r, --repo | Repository for VCS connection. Format of *user/repo* or *organization/repo* | No |
| -d --working-dir | The working directory for the repository. Useful for mono-repos | No
| --oauth-token, -o | Oauth Token **required** for VCS authorization. If you pass -r or --repo, this value must also be passed. You can get this from the **fetch_oauth.py** script. | No |


## Setting Variables

**set_vars.py** script will use a CSV file to set variables on a workspace. It is capable of setting Terraform and Environment variables, as well it can mark them as sensitive.

```
usage: set_vars.py [-h] --workspace WORKSPACE_NAME --file VARS_FILE
```

| Argument | Description | Required |
| --- | ---| --- |
| --workspace | Workspace Name | Yes |
| --file | CSV File | Yes

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