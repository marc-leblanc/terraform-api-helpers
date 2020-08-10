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

def fetchOauth():
    print(f':wrench: Fetching VCS and oauth information ...')

    fetch_oauth_url = f'https://{TFE_ADDRESS}/api/v2/organizations/{TFE_ORGANIZATION}/oauth-clients'

    headers = {'Authorization': 'Bearer ' + TFE_API_TOKEN, 'Content-Type': 'application/vnd.api+json'}

    r = requests.get(fetch_oauth_url,headers = headers)

    if r.status_code == 200:
        print(f':white_check_mark: Pulled VCS information for [bold]{TFE_ORGANIZATION}[/bold] creation completed...')
    else:
        error_response = f'{r.json()["errors"][0]["status"]}: {r.json()["errors"][0]["title"]}'
        print(f':x: Pulling VCS information for [bold]{TFE_ORGANIZATION}[/bold] creation failed.. got: {error_response}')
    print(f'[bold]VCS Connection Information[/bold]\n---------------')
    for vcs in r.json()["data"]:
        print(f'[bold]Name:[/bold] {vcs["attributes"]["name"]}')
        print(f'[bold]ID:[/bold] {vcs["id"]}')
        print(f'[bold]Token[/bold] {vcs["relationships"]["oauth-tokens"]["data"][0]["id"]}')

def main():

    fetchOauth()


if __name__ == "__main__":
    main()

