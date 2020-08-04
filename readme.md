# Helper Script to set Variables on a Terraform Workspace

**Usage**

`./set_vars.sh -w {workspace_name} -f {key_value_file}`

**Set up**

To use this script, you need to set an environment variables for TFE_ADDRESS, TFE_API_TOKEN and TFE_ORGANIZATION

`
export TFE_ADDRESS=app.terraform.io
export TFE_ORGANIZATION=my_org_name
export TFE_API_TOKEN=***************************
`
**Key Value File**

This is a simple implementation. Simply have 1 key = 1 value per line. [Sample](kv_sample.txt)