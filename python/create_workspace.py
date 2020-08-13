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

    if args.repo is not 0:
        payload = { 'data': { 'attributes': { 'name': args.workspace_name, 'terraform_version': args.tf_version, 'working-directory': args.working_dir, 'vcs-repo': { 'identifier': args.repo, 'oauth-token-id': args.oauth_token, 'branch': '' , 'default-branch': True } }, 'type': 'workspaces' }}
    else:
        payload = {'data': { 'attributes': { 'name': args.workspace_name }, 'type': 'workspaces' }}
    #print(payload) usefulfor debug
    r = requests.post(create_workspace_url, data = json.dumps(payload), headers = headers)

    if r.status_code == 201:
        print(f'[green]:white_check_mark:[/green] Workspace [bold]{args.workspace_name}[/bold] creation completed...')
    else:
        print (r.json())
        error_response = f'{r.json()["errors"][0]["title"]}: {r.json()["errors"][0]["detail"]}'

        print(f'[red]:x:[/red] Workspace [bold]{args.workspace_name}[/bold] creation failed.. got: {error_response}')

def main():
    parser = argparse.ArgumentParser(description='Process workspace arguments.')

    parser.add_argument('--workspace', '-w', dest='workspace_name', required=True,
                        help='sets the name of the workspace to create')

    parser.add_argument('--tf-version', '-t', dest='tf_version',
                        help='(optional) specify version of Terraform for the workspace')

    parser.add_argument('--repo', '-r', dest='repo', default=0,
                        help='(optional) specify version of Terraform for the workspace')

    parser.add_argument('--wd', '-d', dest='working_dir',
                        help='(optional) specify version of Terraform for the workspace')

    parser.add_argument('--ot', '-o', dest='oauth_token',
                        help='(optional) specify version of Terraform for the workspace')

    args = parser.parse_args()
    print(args)

    createWorkspace(args)


if __name__ == "__main__":
    main()