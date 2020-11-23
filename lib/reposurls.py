#given a list of jsons with githubs repos info, get their urls

import json
import re
import os 


def getUrls (repos_jsons_path,repos_urls_output_file):
	# get repos' json files
	repos_jsons = []

	for r, dirs, files in os.walk(repos_jsons_path):
	    for file in files:
	        repos_jsons.append(file)

	# get repos' URLs
	json_contents = []
	urls = [] 

	for file in repos_jsons:
		with open(repos_jsons_path+file,'r') as json_reader:
			json_contents = json.load(json_reader)
			urls.extend([item.get('url') for item in json_contents])
			# print(json_reader.read())
			# print(contents)

	#remove duplicates
	unique_urls = list(set(urls))

	#remove urls that are not github repos
	repos_unique_urls = []

	for url in unique_urls:
		if (re.search(r".*github.com/.*/.*", url)):
			if not (re.search(r".*github.com/.*/.*/.+", url)):
				repos_unique_urls.append(url)

	#write output file
	for url in repos_unique_urls:
		with open(repos_urls_output_file, 'a') as file:
			file.write(url + '\n')


	return repos_unique_urls