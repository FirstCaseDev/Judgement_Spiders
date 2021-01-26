# Scrapy settings for SCindKanoon project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'SCindKanoon'

SPIDER_MODULES = ['SCindKanoon.spiders']
NEWSPIDER_MODULE = 'SCindKanoon.spiders'
MONGO_URI = 'mongodb+srv://PuneetShrivas:admin@betatesting.nsnxl.mongodb.net/<dbname>?retryWrites=true&w=majority'
MONGO_DATABASE = 'courtdata'

#  new URI mongodb+srv://PuneetShrivas:admin@betatesting.nsnxl.mongodb.net/test?authSource=admin&replicaSet=atlas-mr0go1-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'SCindKanoon (+http://www.yourdomain.com)'
USER_AGENT = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
# PROXY_POOL_ENABLED = True
# Obey robots.txt rules
ROBOTSTXT_OBEY = False
# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 8
DOWNLOAD_DELAY = 3
# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16


# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# DOWNLOAD_DELAY = 0.1
# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}
DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = 'scrapy.squeues.PickleFifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.FifoMemoryQueue'



# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'SCindKanoon.middlewares.ScindkanoonSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'SCindKanoon.middlewares.ScindkanoonDownloaderMiddleware': 543,
#}
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    # 'scrapy_proxy_pool.middlewares.ProxyPoolMiddleware': 610,
    # 'scrapy_proxy_pool.middlewares.BanDetectionMiddleware': 620,
    # 'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    # 'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
    'SCindKanoon.middlewares.TooManyRequestsRetryMiddleware': 543,

}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'SCindKanoon.pipelines.ScindkanoonPipeline': 300,
}

DUPEFILTER_DEBUG = True

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
RETRY_ENABLED = True
RETRY_TIMES = 8
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429]

ROTATING_PROXY_LIST = [
    '193.149.225.224:80',
    '51.75.147.33:3128',
    '191.101.39.27:80',
    '51.81.82.175:80',
    '103.218.240.75:80',
    '52.149.152.236:80',
    '191.101.39.2:80',
    '192.109.165.239:80',
    '74.143.245.221:80',
    '89.187.177.97:80',
    '89.187.177.103:80',
    '89.187.177.104:80',
    '185.198.188.52:8080',
    '51.158.180.179:8811',
    '89.187.177.100:80',
    '51.116.234.251:3128',
    '91.89.89.11:8080',
    '89.187.177.98:80',
    '89.187.177.88:80',
    '89.187.177.93:80',
    '89.187.177.91:80',
    '89.187.177.92:80',
    '89.187.177.107:80',
    '89.187.177.90:80',
    '89.187.177.85:80',
    '89.187.177.94:80',
    '51.158.186.242:8811',
    '136.243.254.196:80',
    '20.50.107.111:80',
    '88.198.24.108:8080',
    '103.227.255.43:80',
    '103.240.77.98:30093',
    '208.80.28.208:8080',
    '1.10.188.52:32163',
    '40.121.91.147:80',
    '89.107.197.173:35615',
    '152.67.16.49:80',
    '162.144.105.45:3838',
    '103.115.14.156:80',
    '157.230.103.91:34354',
    '60.246.7.4:8080',
    '118.99.100.192:8080',
    '110.74.199.16:63141',
    '150.109.32.166:80',
    '95.31.119.210:31135',
    '103.152.5.70:8080',
    '139.59.122.42:8118',
    '1.4.157.35:46944',
    '182.16.171.42:43188',
    '187.243.253.2:8080',
    '103.115.14.153:80',
    '201.217.49.2:80',
    '2.144.247.25:3128',
    '51.75.147.35:3128',
    '118.173.232.61:47115',
    '213.230.69.33:8080',
    '122.15.131.65:57873',
    '34.121.143.147:80',
    '196.25.237.218:30930',
    '31.179.224.42:44438',
    '85.30.215.48:32946',
    '162.144.48.236:3838',
    '94.130.179.24:8009',
    '109.193.195.2:8080',
    '46.105.122.177:80',
    '103.115.164.99:8080',
    '186.47.82.6:41430',
    '185.198.188.50:8080',
    '201.217.4.101:53281',
    '110.44.122.214:55443',
    '46.35.248.160:55443',
    '37.120.200.102:80',
    '37.120.200.104:80',
    '37.120.200.106:80',
    '37.120.200.108:80',
    '40.79.26.139:1080',
    '43.245.202.15:57396',
    '165.227.71.60:80',
    '191.101.39.237:80',
    '96.9.73.80:56891',
    '118.99.104.25:8080',
    '103.250.157.34:44611',
    '191.96.42.80:8080',
    '191.96.71.118:3128',
    '89.187.177.108:80',
    '89.187.177.99:80',
    '13.233.30.162:80',
    '167.71.5.83:8080',
    '202.45.146.210:80',
    '162.144.50.197:3838',
    '46.4.96.137:3128',
    '88.198.50.103:8080',
    '109.74.37.83:8080',
    '177.22.107.15:8080',
    '171.97.12.148:8080',
    '206.189.223.70:3128',
    '78.137.71.89:8080',
    '194.143.249.175:8080',
    '101.255.134.91:8080',
    '182.253.168.2:8080',
    '62.133.130.206:3128',
    '101.51.73.210:8888',
    '119.93.175.133:8080',
    '37.120.200.107:80',
    '79.125.163.225:30677',
    '134.209.100.73:3128',
    '31.172.105.144:8080',
    '210.212.253.227:8080',
    '163.172.28.22:80',
    '176.9.75.42:8080',
    '78.47.16.54:80',
    '159.138.2.11:80',
    '103.220.204.217:8080',
    '36.94.196.173:8080',
    '162.214.92.202:80',
    '142.93.112.222:3128',
    '203.198.94.132:80',
    '118.175.207.180:40017',
    '150.95.115.224:3128',
    '198.211.100.174:3128',
    '45.8.116.127:8080',
    '202.180.54.211:8080',
    '207.191.165.8:8080',
    '89.187.177.86:80',
    '180.250.12.10:80',
    '162.144.106.245:3838',
    '162.144.46.168:3838',
    '89.187.177.87:80',
    '94.140.115.215:3128',
    '114.23.206.248:8080',
    '112.78.170.27:8080',
    '118.175.93.94:45175',
    '203.202.245.58:80',
    '36.37.177.186:8080',
    '202.154.180.53:46717',
    '188.190.245.135:55443',
    '103.215.177.231:80',
    '177.86.201.22:8080',
    '176.120.37.82:59365',
    '162.144.106.161:3838',
    '162.144.104.137:3838',
    '103.153.66.10:8080',
    '178.217.216.184:49086',
    '185.198.188.49:8080',
    '185.198.188.54:8080',
    '62.213.14.166:8080',
    '37.120.192.154:8080',
    '161.202.226.194:80',
    '37.120.200.110:80',
    '24.172.34.114:49920',
    '197.210.217.66:34808',
    '191.101.39.226:80',
    '191.101.39.81:80',
    '191.101.39.118:80',
    '191.101.39.54:80',
    '193.233.14.18:3128',
    '80.26.96.212:80',
    '191.101.39.185:80',
    '162.144.34.109:3838',
    '187.243.240.54:8080',
    '185.198.188.48:8080',
    '37.120.200.99:80',
    '89.187.177.96:80',
    '36.90.37.6:8080',
    '193.56.255.131:3128',
    '191.101.39.24:80',
    '115.75.1.184:8118',
    '37.152.190.220:80',
    '118.174.232.92:45759',
    '187.130.139.197:8080',
    '195.158.3.198:3128',
    '213.178.39.170:8080',
    '200.94.140.50:30682',
    '105.247.67.115:8080',
    '51.178.49.77:3132',
    '190.167.215.170:52479',
    '79.104.25.218:8080',
    '161.35.4.201:80',
    '191.101.39.170:80',
    '94.244.28.246:31280',
    '139.5.71.70:23500',
    '91.226.5.245:57882',
    '85.237.46.168:53468',
    '188.156.240.240:8118',
    '180.180.156.15:43100',
    '139.59.114.182:8118',
    '178.62.56.172:80',
    '94.73.239.124:55443',
    '51.75.147.43:3128',
    '191.101.39.193:80',
    '192.109.165.129:80',
    '200.62.96.71:80',
    '191.101.39.63:80',
    '89.187.177.106:80',
    '191.101.39.29:80',
    '191.101.39.135:80',
    '93.91.112.247:41258',
    '154.16.63.16:3128',
    '51.158.165.18:8811',
    '192.109.165.139:80',
    '89.187.177.101:80',
    '198.50.163.192:3129',
    '103.115.14.41:80',
    '134.3.255.7:8080',
    '125.25.80.39:42790',
    '110.232.248.37:37764',
    '182.52.90.43:33326',
    '144.217.101.245:3129',
    '175.106.17.62:57406',
    '168.228.51.197:59144',
    '37.49.127.226:8080',
    '128.199.202.122:3128',
    '198.199.86.11:3128',
    '109.193.195.5:8080',
    '192.109.165.35:80',
    '136.233.215.137:80',
    '139.162.78.109:8080',
    '103.25.167.200:53391',
    '5.190.141.137:8080',
    '139.99.102.114:80',
    '193.149.225.228:80',
    '187.216.93.20:55443',
    '191.101.39.191:80',
    '45.7.176.78:49344',
    '92.247.142.182:42367',
    '191.101.39.154:80',
    '103.216.82.153:6666',
    '36.89.228.201:45286',
    '191.101.39.238:80',
    '5.189.133.231:80',
    '188.165.141.114:3129',
    '167.172.203.244:8118',
    '79.137.44.85:3129',
    '36.66.61.7:56232',
    '51.158.119.88:8811',
    '162.144.48.139:3838',
    '62.23.15.92:3128',
    '185.198.188.53:8080',
    '165.22.81.30:46215',
    '185.4.135.147:3128',
    '89.187.177.89:80',
    '197.59.96.202:8080',
    '103.139.156.122:82',
    '180.246.167.78:80',
    '1.10.187.149:44976',
    '104.238.81.186:56227',
    '182.52.90.42:51657',
    '176.63.205.248:54621',
    '80.191.162.2:80',
    '67.225.164.154:80',
    '190.112.136.153:8085',
    '103.47.93.232:51618',
    '154.0.15.166:46547',
    '124.41.211.196:31120',
    '14.192.31.4:50838',
    '50.192.195.69:52018',
    '89.23.198.165:8080',
    '188.120.232.181:8118',
    '118.174.232.239:39258',
    '117.252.219.184:23500',
    '178.33.251.230:3129',
    '158.101.19.129:80',
    '103.113.197.11:8080',
    '178.210.51.118:8080',
    '82.212.62.28:8080',
    '125.26.7.124:61642',
    '37.49.127.232:8080',
    '37.49.127.238:8080',
    '37.49.127.234:8080',
    '176.197.95.2:3128',
    '213.230.127.140:3128',
    '209.97.150.167:3128',
    '138.68.60.8:8080',
    '188.165.16.230:3129',
    '89.187.177.105:80',
    '154.16.202.22:3128',
    '46.5.252.70:8080',
    '95.208.208.237:8080',
    '149.172.255.9:8080',
    '37.49.127.229:8080',
    '134.3.255.4:8080',
    '51.75.147.44:3128',
    '125.141.117.14:80',
    '159.203.61.169:3128',
    '80.48.119.28:8080',
    '202.40.188.94:40486',
    '191.243.53.180:8080',
    '95.156.125.190:41870',
    '150.129.148.99:35101',
    '195.239.115.106:44413',
    '37.79.254.152:3128',
    '24.172.82.94:53281',
    '119.82.252.25:42914',
    '152.67.48.62:3128',
    '118.70.12.171:53281',
    '51.75.147.41:3128',
    '103.115.14.158:80',
    '217.8.51.206:8080',
    '1.10.189.133:40569',
    '91.89.89.9:8080',
]