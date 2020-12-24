from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.browse_all_docs_list import BrowseAllDocsListSpider



process = CrawlerProcess(get_project_settings())
process.crawl(all_list)
process.start() 