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

## To Do (or not)
- Functions functions functions. Usage, payload_push....
- Checking if the variables already exist or not
- Add option to create new/update variables. This currently will error on variables that already exist
- Further data validation, empty lines etc.
