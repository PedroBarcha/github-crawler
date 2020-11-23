# from lib import featuresextract, reposurl, stats
from lib import reposurls
import os 

repos_jsons_path = "repos/json/"
repos_urls_output_file = "repos/urls.txt"

# get repos' URLs (BRADA)
repos_urls = reposurls.getUrls(repos_jsons_path,repos_urls_output_file)

print("Quantidade de repos únicos: "+ str(len(repos_urls)))

#get features for each repo (TK)
# repos_features = []

# for url in repos_urls:
# 	repos_features.extend(featuresextract.extractAll(url)



#stats (GUS)
# ...

