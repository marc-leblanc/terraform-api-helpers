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
    print(f':wrench: Setting variables on {args.workspace_name} ...')
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

    vfile = open(args.vars_file, "r")

    with open(args.vars_file) as vfile:
        reader = csv.reader(vfile) # Create a new reader
        for row in reader:
            print(f'Setting variable [bold]{row[0]}[/bold]....')
            payload={ "data": { "type":"vars", "attributes": { "key":row[0], "value":row[1], "description":row[4], "category":row[3], "hcl":False, "sensitive":row[2] }, "relationships": { "workspace": { "data": { "id":workspace_id, "type":"workspaces" } } } }}
            r = requests.post(set_vars_url, data = json.dumps(payload), headers = headers)
            if r.ok:
                print(f':white_check_mark: OK')
            else:
                error_response = f'{r.json()["errors"][0]["status"]}: {r.json()["errors"][0]["title"]}: {r.json()["errors"][0]["detail"]}'
                print(f':x: Problem setting variable.. got: {error_response}')

    vfile.close()


def main():
    parser = argparse.ArgumentParser(description='Process workspace arguments.')

    parser.add_argument('--workspace', '-w', dest='workspace_name', required=True,
                        help='sets the name of the workspace to create variables in')
    parser.add_argument('--file', '-f', dest='vars_file', required=True,
                        help='sets the variable file to use')
    args = parser.parse_args()

    setVars(args)


if __name__ == "__main__":
    main()