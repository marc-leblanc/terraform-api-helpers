from rich import print
import argparse
import os
import sys
import requests
import json
import csv

try:
    TFE_ADDRESS = os.environ['TFE_ADDRESS']
    TFE_ORGANIZATION = os.environ['TFE_ORGANIZATION']
    TFE_API_TOKEN = os.environ['TFE_API_TOKEN']
except KeyError:
    print (f':exploding_head: [bold red]Error:[/bold red] The following environment variables must be set: TFE_ADDRESS, TFE_ORGANIZATION, TFE_API_TOKEN')
    sys.exit(1)

def setVars(args):
    print(f':wrench: Setting credentials on {args.workspace_name} ...')
    check_workspace_url = f'https://{TFE_ADDRESS}/api/v2/organizations/{TFE_ORGANIZATION}/workspaces/{args.workspace_name}'
    set_vars_url = f'https://{TFE_ADDRESS}/api/v2/vars'

    headers = {'Authorization': 'Bearer ' + TFE_API_TOKEN, 'Content-Type': 'application/vnd.api+json'}

    # Get the Workspace ID/Check if exists
    payload = {'data': { 'attributes': { 'name': args.workspace_name }, 'type': 'workspaces' }}
    r = requests.get(check_workspace_url, headers = headers )

    if r.ok:
        print(f':white_check_mark: Got ID for workspace {args.workspace_name}')
    else:
        error_response = f'{r.json()["errors"][0]["status"]}: {r.json()["errors"][0]["title"]}'
        print(f':x: Problem getting workspace id for {args.workspace_name}.. got: {error_response}')
        sys.exit()
    workspace_id = r.json()["data"]["id"]

    if args.gcp:
        cred = "GOOGLE_CREDENTIALS"
        try:
            CREDENTIALS = os.environ['GOOGLE_CREDENTIALS']
        except KeyError:
            print (f':exploding_head: [bold red]Error:[/bold red] GOOGLE_CREDENTIALS environment variable must be set')
            sys.exit(1)
    elif args.github:
        cred = "GITHUB_PAT"
        try:
            CREDENTIALS = os.environ['GITHUB_PAT']
        except KeyError:
            print(f':exploding_head: [bold red]Error:[/bold red]GITHUB_PAT environment variable must be set')
            sys.exit(1)
    else:
        print(f'[bold red]Error:[/bold red] No Credential type indicated')
        sys.exit(1)

    print(f'Setting [bold]{cred}[/bold] on workspace [bold]{args.workspace_name}[/bold]....')
    payload={ "data": { "type":"vars", "attributes": { "key": cred, "value": CREDENTIALS, "description":"Platform credential", "category": "env", "hcl":False, "sensitive": True }, "relationships": { "workspace": { "data": { "id":workspace_id, "type":"workspaces" } } } }}
    r = requests.post(set_vars_url, data = json.dumps(payload), headers = headers)
    if r.ok:
        print(f':white_check_mark: OK')
    else:
        error_response = f'{r.json()["errors"][0]["status"]}: {r.json()["errors"][0]["title"]}: {r.json()["errors"][0]["detail"]}'
        print(f':x: Problem setting variable.. got: {error_response}')

def main():
    parser = argparse.ArgumentParser(description='Process arguments.')

    parser.add_argument('--workspace', '-w', dest='workspace_name', required=True,
                        help='Workspace to copy the credential to')
    parser.add_argument('--gcp', action='store_true',
                        help='Yes to copy GOOGLE_CREDENTIALS')
    parser.add_argument('--github', action='store_true',
                        help='Yes to copy GITHUB_PAT')
    args = parser.parse_args()

    setVars(args)


if __name__ == "__main__":
    main()