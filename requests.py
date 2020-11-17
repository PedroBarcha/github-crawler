import scrapy

class githubSpider(scrapy.Spider):
	name = "github"

	start_urls = ["https://github.com/scrapy/scrapy/graphs/commit-activity"]

	def parse(self, response):
		import ipdb; ipdb.set_trace()
		pass