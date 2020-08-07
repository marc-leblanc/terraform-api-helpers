from rich import print
import argparse
import os
import sys
import requests
import json

try: 
    TFE_ADDRESS = os.environ['TFE_ADDRESS']
    TFE_ORGANIZATION = os.environ['TFE_ORGANIZATION']
    TFE_API_TOKEN = os.environ['TFE_API_TOKEN']
except KeyError:
    print (f':exploding_head: [bold red]Error:[/bold red] The following environment variables must be set: TFE_ADDRESS, TFE_ORGANIZATION, TFE_API_TOKEN')
    sys.exit(1)

def createWorkspace(args):
    print(f':wrench: Creating Terraform Workspace [bold]{args.workspace_name}[/bold]...')

    create_workspace_url = f'https://{TFE_ADDRESS}/api/v2/organizations/{TFE_ORGANIZATION}/workspaces'
    
    headers = {'Authorization': 'Bearer ' + TFE_API_TOKEN, 'Content-Type': 'application/vnd.api+json'}
    payload = {'data': { 'attributes': { 'name': args.workspace_name }, 'type': 'workspaces' }}
    
    r = requests.post(create_workspace_url, data = json.dumps(payload), headers = headers)

    if r.status_code == 201:
        print(f':white_check_mark: Workspace [bold]{args.workspace_name}[/bold] creation completed...')
    else:
        error_response = f'{r.json()["errors"][0]["title"]}: {r.json()["errors"][0]["detail"]}'

        print(f':x: Workspace [bold]{args.workspace_name}[/bold] creation failed.. got: {error_response}')

def main():
    parser = argparse.ArgumentParser(description='Process workspace arguments.')

    parser.add_argument('--workspace', '-w', dest='workspace_name', required=True,
                        help='sets the name of the workspace to create')
    
    args = parser.parse_args()

    createWorkspace(args)


if __name__ == "__main__":
    main()