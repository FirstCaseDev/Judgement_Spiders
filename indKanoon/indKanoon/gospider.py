from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from indKanoon.spiders.check_update_case_counts import CheckUpdateCaseCountsSpider



process = CrawlerProcess(get_project_settings())
process.crawl(case_counts)
process.start() 