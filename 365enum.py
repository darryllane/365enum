import json
import requests
import argparse

requests.packages.urllib3.disable_warnings()

parser = argparse.ArgumentParser(description='Used to identify if a given set of domains are configured for managed/federated Microsoft services.')
parser.add_argument('--domains', help='Supply a document path containing one domain per line.', required=True)
args = vars(parser.parse_args())


def name_list(filename):
	try:
		name_list = [line.rstrip('\n') for line in open(filename)]
	except Exception as e:
		print(e.args)
	return name_list


def enum(domains):
	data = []
	for domain in domains:
		link = 'https://login.microsoftonline.com/common/userrealm/?user={}&api-version=2.1&checkForMicrosoftAccount=true'.format(domain)

		headers = {"User-Agent" : 'Test',
			       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			       'Accept-Language': 'en-US,en;q=0.5',
			       'Accept-Encoding': 'gzip, deflate'}

		try:
			response = requests.get(link, headers=headers, verify=False)
			json_data = response.json()
			if json_data:

				MicrosoftAccount = json_data['MicrosoftAccount']
				Login = json_data['Login']
				NameSpaceType = json_data['NameSpaceType']
				TenantBrandingInfo = json_data['TenantBrandingInfo']
				IsMicrosoftAccountSet = json_data['IsMicrosoftAccountSet']
				DomainName = json_data['DomainName']
				FederationBrandName = json_data['FederationBrandName']
				cloud_instance_name = json_data['cloud_instance_name']
				if 'federation_protocol' in json_data:
					federation_protocol = json_data['federation_protocol']
				if 'AuthURL' in json_data:
					AuthURL = json_data['AuthURL']

				if 'federation_protocol' in json_data and 'AuthURL' in json_data:
					data.append(({'AuthURL':AuthURL, 'federation_protocol':federation_protocol, 'MicrosoftAccount':MicrosoftAccount, 'Login':Login, 'NameSpaceType':NameSpaceType, 'TenantBrandingInfo':TenantBrandingInfo, 'IsMicrosoftAccountSet':IsMicrosoftAccountSet, 'DomainName':DomainName, 'FederationBrandName':FederationBrandName, 'cloud_instance_name':cloud_instance_name}))

				else:
					data.append(({'MicrosoftAccount':MicrosoftAccount, 'Login':Login, 'NameSpaceType':NameSpaceType, 'TenantBrandingInfo':TenantBrandingInfo, 'IsMicrosoftAccountSet':IsMicrosoftAccountSet, 'DomainName':DomainName, 'FederationBrandName':FederationBrandName, 'cloud_instance_name':cloud_instance_name}))

			for dat in data:
				if 'federation_protocol' in str(dat):
					print('Domain: {}\nType: {}\nFederationBrandName: {}\nFederationProtocol: {}\nAuthURL: {}\n'.format(dat['DomainName'], dat['NameSpaceType'], dat['FederationBrandName'], dat['federation_protocol'], dat['AuthURL']))
				else:
					print('Domain: {}\nType: {}\nFederationBrandName: {}\n'.format(dat['DomainName'], dat['NameSpaceType'], dat['FederationBrandName']))

		except Exception as e:
			pass


domains = name_list(args['domains'])
enum(domains)
