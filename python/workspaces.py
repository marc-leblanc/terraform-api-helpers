from rich import print
from prettytable import PrettyTable
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

    if r.ok:
        print(f'[green]:white_check_mark:[/green] Workspace [bold]{args.workspace_name}[/bold] creation completed...')
    else:
        #print (r.json())
        error_response = f'{r.json()["errors"][0]["title"]}: {r.json()["errors"][0]["detail"]}'
        print(f'[red]:x:[/red] Workspace [bold]{args.workspace_name}[/bold] creation failed.. got: {error_response}')

# Function: listWorkspaces()
#           Simply lists the workspaces for the organization, shows the vcs repo if attached, the working
#           directory if set and the date created

def listWorkspaces():
    ls_url = f'https://{TFE_ADDRESS}/api/v2/organizations/{TFE_ORGANIZATION}/workspaces'
    headers = {'Authorization': 'Bearer ' + TFE_API_TOKEN, 'Content-Type': 'application/vnd.api+json'}
    r = requests.get(ls_url,headers = headers)

    if r.ok:
        t = PrettyTable([f'[bold]Workspace Name[/bold]', 'VCS Repo', 'Working Directory', 'Date Created'])
        t.align = "l"
        workspaces = r.json()["data"]
        for workspace in workspaces:
            name = workspace["attributes"]["name"]
            if workspace["attributes"]["vcs-repo"]:
                vcsRepo = workspace["attributes"]["vcs-repo"]["identifier"]
            else:
                vcsRepo = ""
            dateCreated = workspace["attributes"]["created-at"]
            workingDir = workspace["attributes"]["working-directory"]
            t.add_row([name, vcsRepo, workingDir, dateCreated])
        print(t)
    else:
        print (r.json())
        error_response = f'{r.json()["errors"][0]["title"]}: {r.json()["errors"][0]["detail"]}'

def main():
    parser = argparse.ArgumentParser(description='Process workspace arguments.')

    parser.add_argument('--workspace', '-w', dest='workspace_name',
                        help='sets the name of the workspace to create')
    parser.add_argument('--tf-version', '-t', dest='tf_version',
                        help='(optional) specify version of Terraform for the workspace')
    parser.add_argument('--repo', '-r', dest='repo', default=0,
                        help='(optional) specify version of Terraform for the workspace')
    parser.add_argument('--working-dir', '-d', dest='working_dir',
                        help='(optional) specify version of Terraform for the workspace')
    parser.add_argument('--oauth-token', '-o', dest='oauth_token',
                        help='(optional) specify version of Terraform for the workspace')
    parser.add_argument('--list', action='store_true',
                        help='List workspaces for the Organization')
    parser.add_argument('--create', action='store_true',
                        help='Create a workspace for the Organization')
    args = parser.parse_args()

    if(args.list):
        listWorkspaces()
    elif(args.create):
        createWorkspace(args)

if __name__ == "__main__":
    main()