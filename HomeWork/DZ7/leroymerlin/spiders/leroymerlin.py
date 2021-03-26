import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from HomeWork.DZ7.leroymerlin.items import LeroymerlinItem


class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search):
        super(LeroymerlinSpider, self).__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']

    def parse(self, response: HtmlResponse):
        links = response.xpath('//a[@slot="name"]')
        for link in links:
            yield response.follow(link, callback=self.parse_good)
        next_page = response.xpath('//a[@rel="next"]/@href').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_good(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroymerlinItem(), response=response)
        loader.add_xpath('title', '//h1[@slot="title"]/text()')
        loader.add_xpath('type', '//div[@class="def-list__group"]/dt/text()')
        loader.add_xpath('specifications', '//div[@class="def-list__group"]/dd/text()')
        loader.add_xpath('photos', '//img[contains(@slot, "thumbs")]/@src')
        loader.add_xpath('art', '//span[@slot="article"]/@content')

        yield loader.load_item()
