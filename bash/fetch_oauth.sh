#! /bin/bash

# Helper script to fetch configured VCS connection information on TFE/TF Cloud via API. 

# Required environment variables:
# TFE_ADDRESS = TFE Hostname
# TFE_API_TOKEN = Your user or Team API token as generated from TFE
# TFE_ORGANIZATION = The Organization in TFE the workspace is part of
# 

# Fetch Oauth clients 
oauth_clients=`curl \
  --header "Authorization: Bearer $TFE_API_TOKEN" \
  --header "Content-Type: application/vnd.api+json" \
  --request GET \
  https://$TFE_ADDRESS/api/v2/organizations/$TFE_ORGANIZATION/oauth-clients 2>/dev/null`


printf "VCS Connnections:\n-----------------\n\n"
#Display VCS Information 
for row in $(echo "${oauth_clients}" | jq -r '.data[] | @base64'); do
    _jq() {
     echo ${row} | base64 --decode | jq -r ${1}
    }
   # Fetch Oauth token
   token=`curl \
  --header "Authorization: Bearer $TFE_API_TOKEN" \
  https://$TFE_ADDRESS/api/v2/oauth-clients/$(_jq '.id')/oauth-tokens 2>/dev/null |tac |tac |jq -r '.data[0].id'`
 printf "Name: $(_jq '.attributes.name')\n"
   printf "ID: $(_jq '.id')\n"
 printf "Token: $token\n\n"

done
