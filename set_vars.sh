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
error=0
error_descrip=""

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
   printf "Please set TFE_ADDRESS environment variable \n"
   exit
fi

# Check for the TFE API Token env ariable. Die if not set.
if [[ -z "${TFE_API_TOKEN}" ]]; then
   printf "Please set the TFE_API_TOKEN environment variable \n"
   exit
fi

# Check for the TFE Organization env ariable. Die if not set.
if [[ -z "${TFE_ORGANIZATION}" ]]; then
   printf "Please set the TFE_API_TOKEN environment variable \n"
   exit
fi

# Get the Workspace ID

workspace_id=`curl \
  --header "Authorization: Bearer $TFE_API_TOKEN" \
  --header "Content-Type: application/vnd.api+json" \
  https://$TFE_ADDRESS/api/v2/organizations/$TFE_ORGANIZATION/workspaces/$w |tac |tac |jq -r '.data.id'`



# Check if we got a workspace ID back
if [[ $workspace_id == 'null' ]] ; then  
    printf "Workspace $w could not be found in $TFE_ORGANIZATION. Plase double check the workspace name, organization name and access \n"
    exit
fi

# Loop over csv file
while read line; do
  # Parse out values by comma, preserve spaces with +++++ string substitution 
  set -- `echo $line | sed 's/ /+++++/g' | tr ',' " "`
  
  key=$1
  value=$2
  sensitive=$3
  category=$4
  description=`echo $5 |sed 's/+++++/ /g'` #change +++++ back to spaces

  # Data Validation
  if [[ $key =~ ['!@#$%^&*()_+'] ]]; then
    error=1
    error_descrip+=" - 'Key' must not contain special characters \n"
  fi

  if [[ $sensitive != 'true' ]] && [[ $sensitive != 'false' ]] ; then
    error=1
    error_descrip+=" - 'Sensitive' must be either (true|false) \n"
  fi

  if [[ $category != 'terraform' ]] && [[ $category != 'env' ]] ; then
    error=1
    error_descrip+="'Category' must be either ('env'|'terraform') \n"
  fi

  # Create they API payload
  if [[ $error -ne 0 ]]; then
    printf "Error on key $key: \n$error_descrip \n"
  else

  payload="{
  \"data\": {
    \"type\":\"vars\",
    \"attributes\": {
      \"key\":\"$key\",
      \"value\":\"$value\",
      \"description\":\"$description\",
      \"category\":\"$category\",
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
printf "Creating variable $key. \n Result: \n"

curl -s \
  --header "Authorization: Bearer $TFE_API_TOKEN" \
  --header "Content-Type: application/vnd.api+json" \
  --request POST \
  --data "$payload" \
  https://$TFE_ADDRESS/api/v2/vars
  echo ""
fi   
# Blank values
error=0
error_descrip=""
key=""
value=""
category="terraform"
description="variable"
sensitive="false"
done < $f 