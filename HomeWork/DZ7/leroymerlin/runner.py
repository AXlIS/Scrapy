from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess

import settings
from spiders.leroymerlin import LeroymerlinSpider
import click


@click.command()
@click.option('--search', default='столы')
def runner(search):
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroymerlinSpider, search=search)

    process.start()


if __name__ == '__main__':
    runner()
