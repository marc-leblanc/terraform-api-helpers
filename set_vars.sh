#! /bin/bash

# Helper script for setting variables on TFE/TF Cloud via API. 
#
# This script can:
#       - set Terraform variables on a workspace
#       - set variable descriptions
#       - set the variable to sensitive
#
# Required environment variables:
# TFE_ADDRESS = TFE Hostname
# TFE_API_TOKEN = Your user or Team API token as generated from TFE
# TFE_ORGANIZATION = The Organization in TFE the workspace is part of
# 
# Required input variables
# -w = workspace name
# -f = KV file (path/filename)

set -e
set -u

w=""
f="" 

# Get Options 
# w = workspace name
# f = KV file
while getopts ":w:f:" OPT; do

  case ${OPT} in
    w )
      w=$OPTARG
      ;;
    f ) 
      f=$OPTARG
      ;;
    : )
      echo
      echo " Error: option -${OPTARG} requires an argument"
      exit
      ;;
   \? )
      echo
      echo " Error: invalid option -${OPTARG}"
      exit
      ;;
  esac
done
shift $((OPTIND -1))


# Check for the TFE Address env variable. Die if not set.
if [[ -z "${TFE_ADDRESS}" ]]; then
   echo "Please set TFE_ADDRESS environment variable"
   exit
fi

# Check for the TFE API Token env ariable. Die if not set.
if [[ -z "${TFE_API_TOKEN}" ]]; then
   echo "Please set the TFE_API_TOKEN environment variable"
   exit
fi

# Check for the TFE Organization env ariable. Die if not set.
if [[ -z "${TFE_ORGANIZATION}" ]]; then
   echo "Please set the TFE_API_TOKEN environment variable"
   exit
fi

# Get the Workspace ID

workspace_id=`curl \
  --header "Authorization: Bearer $TFE_API_TOKEN" \
  --header "Content-Type: application/vnd.api+json" \
  https://$TFE_ADDRESS/api/v2/organizations/$TFE_ORGANIZATION/workspaces/$w |tac |tac |jq -r '.data.id'`

# Loop over KV file
while read line; do
  # Parse out values by comma 
  set -- `echo $line | tr ',' ' '`
  vars=$1
  sensitive=$2
  description=$3
  
  # Split the Variable/Value
  set -- `echo $vars | tr '=' ' '`
  key=$1
  value=$2

  # Create they API payload
  payload="{
  \"data\": {
    \"type\":\"vars\",
    \"attributes\": {
      \"key\":\"$key\",
      \"value\":\"$value\",
      \"description\":\"$description\",
      \"category\":\"terraform\",
      \"hcl\":false,
      \"sensitive\":$sensitive
    },
    \"relationships\": {
      \"workspace\": {
        \"data\": {
          \"id\":\"$workspace_id\",
          \"type\":\"workspaces\"
        }
      }
    }
  }
}"
echo "Creating variable $key. Result: "
echo ""
curl -s \
  --header "Authorization: Bearer $TFE_API_TOKEN" \
  --header "Content-Type: application/vnd.api+json" \
  --request POST \
  --data "$payload" \
  https://$TFE_ADDRESS/api/v2/vars
  echo ""
done < $f 