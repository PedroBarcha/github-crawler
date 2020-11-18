from lib import featuresextract, crawler, stats

#each urls must contain a list of github repos
init_urls = ["https://github.com/sindresorhus/awesome"]
# init_urls = ["https://github.com/trending", "https://github.com/ogwurujohnson/Awesome-Repos"]

#crawl for repos' URLs
# repo_urls = []
# for init_url in init_urls
	# repo_urls.extend(crawler.crawl(init_url))

#get features for each repo
# repos_features = []
# for repo_url in repo_urls:
# 	repos_features.extend(featuresextract.extractAll(repo_url))

#stats
# ...

