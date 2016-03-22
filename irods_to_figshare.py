import argparse
import requests
import json
import hashlib
import os

from irods.session import iRODSSession



#load config
config = json.loads(open('irods_figshare.conf.json').read())

#argument parser
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('file', help="iRODS file to work on")
args = arg_parser.parse_args()

#irods stuff
irods_session = iRODSSession(host=config['irods']['host'],
			     port=config['irods']['port'],
                             user=config['irods']['user'],
                             password=str(config['irods']['passwd']),
                             zone=config['irods']['zone'])

irods_collection = irods_session.collections.get(config['irods']['collection'])

#figshare stuff
access_token = config['figshare']['access_token']
api_endpoint = config['figshare']['api_endpoint']

#request session
http_session = requests.Session()
api_headers = {
        "Authorization": "token {}".format(access_token),
        "Content-Type": "application/json"
}
http_session.headers.update(api_headers)

#lets get the file and associated metadata
file_path = os.path.join(config['irods']['collection'], args.file)
file_obj = irods_session.data_objects.get(file_path)
file_metadata = file_obj.metadata.items()

#create article
article_metadata = {
	"title": "",
	"description": "",
	"tags": ""
}

for meta in file_metadata:
    name = meta.name.lower()
    if name == "title":
        article_metadata["title"] = meta.value
    elif name == "description":
        article_metadata["description"] = meta.value
    elif name == "tags":
        article_metadata["tags"] = meta.value.split(',')
    else:
        continue

article_create_endpoint = "{}/account/articles".format(api_endpoint)
request = http_session.post(article_create_endpoint, data=json.dumps(article_metadata), headers=api_headers)
article_id = request.headers["Location"].split('/')[-1]

#Add file to article - upload file
##initiate upload

m = hashlib.md5()
with file_obj.open('r') as fd:
	for line in fd:
	    m.update(line)
	fd.seek(0, 0)
md5sum = m.hexdigest()

file_data = {
	"name": file_obj.name,
	"size": file_obj.size,
	"md5": md5sum
}

create_file_endpoint = "{}/account/articles/{}/files".format(api_endpoint, article_id)
request = http_session.post(create_file_endpoint, data=json.dumps(file_data))
file_url = '{location}'.format(**request.json())
file_id = file_url.split('/')[-1]

file_info = http_session.get(file_url).json()
file_parts = http_session.get(file_info["upload_url"]).json()["parts"]

with file_obj.open('r') as fd:
    for part in file_parts:
        size = part['endOffset'] - part['startOffset'] + 1
        address = '{}/{}'.format(file_info['upload_url'], part['partNo'])
        http_session.put(address, data=fd.read(size))

#complete file
file_completed = http_session.post(file_url)

print "Done!"
print "Check out the article at {}/{}?access_token={}".format(article_create_endpoint, article_id, access_token)
print "Check out the file at {}/{}/files/{}?access_token={}".format(article_create_endpoint, article_id, file_id, access_token)

