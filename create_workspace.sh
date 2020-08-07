#! /bin/bash

# Helper script for creating Worskpaces on TFE/TF Cloud via API. 
#
# This script can:
#       - create a workspace
#       - attach a repo
#       - set variables on the workspace via set_vars.sh script 
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
r=""
o=""
f="" 
error=0
error_descrip=""


# Get Options 
# w = workspace name
# r = repo (user/repo format)
# o = oauth token - get with fetch_oauth.sh
# f = CSV file for variables

while getopts ":w:f:r:o:" OPT; do

  case ${OPT} in
    w )
      w=$OPTARG
      ;;
    f ) 
      f=$OPTARG
      ;;
    r) 
      r=$OPTARG
      ;;
    o )
      o=$OPTARG
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
  https://$TFE_ADDRESS/api/v2/organizations/$TFE_ORGANIZATION/workspaces/$w 2>/dev/null |tac |tac |jq -r '.data.id'`



# Check if we got a workspace ID back
if [[ $workspace_id != 'null' ]] ; then  
    printf "Workspace $w already exists in $TFE_ORGANIZATION. Nothing to do. \n"
    exit
fi

if [[ -z $r ]]; then
# if no repo was passed as -r, create a basic workspace
  payload="{
    \"data\": {
      \"attributes\": {
        \"name\": \"$w\"
      },
      \"type\": \"workspaces\"
    }
  }"
else 
# Create a VCS backed repo - requires -r for repo and -ot for oauth token 
  payload="{
  \"data\": {
    \"attributes\": {
      \"name\": \"$w\",
      \"terraform_version\": \"0.11.1\",
      \"working-directory\": \"\",
      \"vcs-repo\": {
        \"identifier\": \"$r\",
        \"oauth-token-id\": \"$o\",
        \"branch\": \"\",
        \"default-branch\": true
      }
    },
    \"type\": \"workspaces\"
  }
  }"  
fi

printf "Creating worskapce  $w. \n Result: \n"

curl -s \
  --header "Authorization: Bearer $TFE_API_TOKEN" \
  --header "Content-Type: application/vnd.api+json" \
  --request POST \
  --data "$payload" \
  https://$TFE_ADDRESS/api/v2/organizations/$TFE_ORGANIZATION/workspaces 2>/dev/null
  echo ""

# If file var is set, setup the ars
if [[ ! -z "$f" ]]; then
  ./set_vars.sh -w $w -f $f
fi