import scrapy
from scrapy.http import HtmlResponse
from HomeWork.DZ6.hhparser.items import SuperjobItem


class SuperjobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bt%5D%5B0%5D=4']

    def parse(self, response: HtmlResponse):
        links = response.xpath('//a[contains(@class, "icMQ_ _6AfZ9")]/@href').extract()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parser)
        next_page = response.xpath('//a[contains(@class, "f-test-link-Dalshe")]/@href').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vacancy_parser(self, response: HtmlResponse):
        title = response.xpath('//h1/text()').extract_first()
        salary = response.xpath('//span[@class="_1OuF_ ZON4b"]/span/span[contains(@class, "_2Wp8I")]/text()').extract()
        yield SuperjobItem(title=title, salary=salary, link=response.url)
