import scrapy
from scrapy.http import HtmlResponse
from HomeWork.DZ6.hhparser.items import HhparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = [
        'https://hh.ru/search/vacancy?L_save_area=true&clusters=true&enable_snippets=true&text=python&showClusters=true']

    def parse(self, response: HtmlResponse):
        links = response.xpath('//a[@data-qa="vacancy-serp__vacancy-title"]/@href').extract()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)
        next_page = response.css("a.HH-Pager-Controls-Next::attr('href')").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(self, response: HtmlResponse):
        title = response.xpath("//h1//text()").extract_first()
        salary = response.xpath('//p[@class="vacancy-salary"]/span/text()').extract()
        yield HhparserItem(title=title, salary=salary, link=response.url)
