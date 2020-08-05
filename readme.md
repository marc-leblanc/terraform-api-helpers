# Helper Script to set Variables on a Terraform Workspace

**Usage**

`./set_vars.sh -w {workspace_name} -f {key_value_file}`

**Set up**

To use this script, you need to set an environment variables for TFE_ADDRESS, TFE_API_TOKEN and TFE_ORGANIZATION

```
export TFE_ADDRESS=app.terraform.io
export TFE_ORGANIZATION=my_org_name
export TFE_API_TOKEN=***************************
```

**Key Value File**

In the form of 
```
var=value,sensitive(true|false),some description
foo=bar,true,this variable is sensitive
bar=foo,false,this variable is not sensitive
```

[Example File](kv_sample.txt)

## To Do (or not)
- input validation
- Variable types to allow setting Environment variables
- Checking if the variables already exist or not
