## irods_figshare
playground for irods figshare integration.

`irods_to_figshare.py` script is a PoC for copying files from iRODS to figshare via the figshare API.

## Figshare access token
Create a figshare account, login and then access the Aplications section. There you can generate a Personal Access token that can be used to access the figshare API.

## Required configuration
Check out `irods_figshare.conf.json` for some sample values.

## Running the script
Requires `python-irodsclient` available [here](https://github.com/iPlantCollaborativeOpenSource/python-irodsclient).
Make sure that the file passed as argument to the script exists in iRODS and that it has associated the following metadata fields:
`title`, `description`, `tags`. The script will search for and use these in order to create the figshare article.

Execute the script: `python irods_to_figshare.py figshare_test.txt`

