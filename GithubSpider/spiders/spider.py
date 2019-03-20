import scrapy
from GithubSpider.items import GithubRepoItem

class GithubTopicSpider(scrapy.Spider):
    name = "topic_spider"
    repo_cnt = 0
    page_cnt = 0

    def start_requests(self):
        if self.topic is None:
            self.topic = 'ros'
        if self.max_page is None:
            self.max_page = 1
        yield scrapy.Request('https://github.com/topics/'+self.topic)

    def parse(self, response):
        self.page_cnt += 1
        if self.page_cnt > self.max_page:
            return

        for art in response.xpath('//article'):
            url_suffix = art.xpath('div[@class="d-flex flex-justify-between flex-items-start mb-1"]/h3/a/@href').extract_first()
            url = response.urljoin(url_suffix)
            yield scrapy.Request(url, callback=self.parse_repo)
        url = response.url
        formxpath = '//form[@class="ajax-pagination-form js-ajax-pagination"]'
        # Load More
        if response.xpath(formxpath):
            yield scrapy.FormRequest.from_response(response, formxpath=formxpath, url=url, callback=self.parse)

    def parse_repo(self, response):
        self.repo_cnt += 1
        name = response.xpath('//strong[@itemprop="name"]//text()').extract_first()
        repo_url = response.xpath('//clipboard-copy/@value').extract_first()
        owner_name = repo_url.split('/')[3]
        # Tag
        tags = response.xpath('//div[@class="list-topics-container f6"]/a/text()').extract()
        tags = [tag.strip() for tag in tags]

        repo_item = GithubRepoItem()
        repo_item['name'] = name
        repo_item['owner_name'] = owner_name
        repo_item['repo_url'] = repo_url
        repo_item['tags'] = tags
        yield repo_item