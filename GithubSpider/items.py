# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GithubspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class GithubRepoItem(scrapy.Item):
	name = scrapy.Field()
	owner_name = scrapy.Field()
	git_url = scrapy.Field()
	tags = scrapy.Field()