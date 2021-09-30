import requests
import json

api_key = "[YOUR API KEY]"
header = {"Authorization":"Bearer %s" % (api_key)}

def getUserfromApiKey():
	url = "https://api.pipedream.com/v1/users/me"
	r = requests.get(url, headers=header)
	if r.status_code == 200:
		parseData = json.loads(r.text)
		print("[+] ID: " + parseData['data']['id'])
		print("[+] Username: " + parseData['data']['username'])
		print("[+] Email: " + parseData['data']['email'])

def getSourcefromUser():
	url = "https://api.pipedream.com/v1/users/me/sources"
	r = requests.get(url, headers=header)
	if r.status_code == 200:
		parseData = json.loads(r.text)
		print("[*] Your Sources: \r\n")
		for x in range(len(parseData['data'])):
			ID = str(x)
			SourceID = parseData['data'][x]['id']
			Name = parseData['data'][x]['name']
			URL = parseData['data'][x]['configured_props']['http']['endpoint_url']
			print("[+] ID: %s \r\nSource ID: %s \r\nName: %s \r\nURL: %s \r\n" % (ID,SourceID,Name,URL))
		getSourceID = input('$ Please Choose ID: ')
		return parseData['data'][int(getSourceID)]['id']

def getEventfromSourceID(src_id):
	url = "https://api.pipedream.com/v1/sources/%s/events" % (src_id)
	r = requests.get(url, headers=header)
	if r.status_code == 200:
		parseData = json.loads(r.text)
		print("[*] Request from %s: \r\n" % (parseData['data'][0]['e']['headers']['host']))
		for x in range(len(parseData['data'])):
			X_Forward_For = parseData['data'][x]['e']['headers']['x-forwarded-for']
			X_Forward_Proto = parseData['data'][x]['e']['headers']['x-forwarded-proto']
			X_Forward_Port = parseData['data'][x]['e']['headers']['x-forwarded-port']
			User_Agent = parseData['data'][x]['e']['headers']['user-agent']
			if 'referer' in parseData['data'][x]['e']['headers']:
				Referer = parseData['data'][x]['e']['headers']['referer']
			else:
				Referer = 'None'
			Path = parseData['data'][x]['e']['path']
			Query = parseData['data'][x]['e']['query']
			print("""[*] Headers: \r\n X-forwarded-for: %s \r\n x-forwarded-port: %s \r\n x-forwarded-proto: %s \r\n Referer: %s \r\n User-Agent: %s \r\n[*] Path: %s \r\n[*] Query: %s \r\n"""
			% (X_Forward_For,X_Forward_Port,X_Forward_Proto,Referer,User_Agent,Path,Query))
if __name__ == '__main__':
	getUserfromApiKey()
	sourceid = getSourcefromUser()
	getEventfromSourceID(sourceid)
