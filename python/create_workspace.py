from rich import print
import argparse
import os
import requests
import json

TFE_ADDRESS = os.environ['TFE_ADDRESS']
TFE_ORGANIZATION = os.environ['TFE_ORGANIZATION']
TFE_API_TOKEN = os.environ['TFE_API_TOKEN']

def createWorkspace(args):
    print(f':wrench: Creating Terraform Workspace [bold]{args.workspace_name}[/bold]...')

    create_workspace_url = f'https://{TFE_ADDRESS}/api/v2/organizations/{TFE_ORGANIZATION}/workspaces'
    
    headers = {f'Authorization': 'Bearer {TFE_API_TOKEN}', 'Content-Type': 'application/vnd.api+json'}
    payload = { 'data': { 'attributes': { 'name': args.workspace_name }, 'type': 'workspaces' } }

    r = requests.post(create_workspace_url, data = json.dumps(payload), headers = headers)
    
    if r.status_code == 201:
        print(f':white_check_mark: Workspace [bold]{args.workspace_name}[/bold] creation completed...')
    else:
        print(f':x: Workspace [bold]{args.workspace_name}[/bold] creation failed...')

def main():
    parser = argparse.ArgumentParser(description='Process workspace arguments.')

    parser.add_argument('--workspace', dest='workspace_name',
                        help='sets the name of the workspace to create')
    
    args = parser.parse_args()

    createWorkspace(args)

if __name__ == "__main__":
    main()