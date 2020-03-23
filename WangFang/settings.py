# Scrapy settings for WangFang project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'WangFang'

SPIDER_MODULES = ['WangFang.spiders']
NEWSPIDER_MODULE = 'WangFang.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'WangFang (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  # 'Accept-Language': 'en',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    'Cookie': 'Hm_lvt_838fbc4154ad87515435bf1e10023fab=1569052465,1569055013,1569131615,1569149726; zh_choose=n; firstvisit_backurl=http%3A//www.wanfangdata.com.cn; Hm_lvt_f5e6bd27352a71a202024e821056162b=1569200543; Hm_lpvt_f5e6bd27352a71a202024e821056162b=1569200543; WFKS.Auth=%7b%22Context%22%3a%7b%22AccountIds%22%3a%5b%5d%2c%22Data%22%3a%5b%5d%2c%22SessionId%22%3a%224259a941-42bf-4430-b122-d6eb9a637829%22%2c%22Sign%22%3a%22hi+authserv%22%7d%2c%22LastUpdate%22%3a%222019-09-23T01%3a01%3a57Z%22%2c%22TicketSign%22%3a%22nzGc4NB%5c%2f0aAuBY5KgNFCxQ%3d%3d%22%7d; SEARCHHISTORY_0=UEsDBBQACAgIAJRIN08AAAAAAAAAAAAAAAABAAAAMO3afU%2FbRhgA8O8SyfzFqM%2F2vSGhyXmDtIWG%0AklBgmiaTOC%2BQOCFxCGWqRKWKIrZqZVs3qUXbOm10m9R2U6Wt7druw4yE7FvssUMHBNsB2rpEnYTE%0AxT6j%2BMfdc89z9gcfB0xttqCPaUU9MGjUCoX%2BQD4dGAyUi%2Bdmo7NpU%2BFyoD9Qq%2BqVWPplh6quVVK5%0AxOUyXILgZKUAF%2BRMszx45ky9Xh%2Boa0ZGM7JpzdQGUqXiQMo4075k99f5fNUcSJfe3%2Fs7Q2W9ki%2FF%0AjEypr5or1e1DfWUtq0%2Fkl%2FUhSexrd71UqqSHhAgReEjgUSGCBcYEpvblq4lKPpvVKwktOwRfV18q%0AV%2FRqNV8y4Is1N79trK3DUdP%2BwnufjVoxWqoZcFtY7A%2BkKrpm6om85YAw4ZIoEorg9q%2F0uxkNx4yR%0AsVhpSuHUN6M9n7RuavmCl1JQFji2lIIRgQW7KD261XjxiacSI1iUmaOUyDgguEvxkeh8bmo0LSPJ%0AD6mCns1XC5oJt1b1DezRrda9awfAEJYZPeyFOKdMAQp3r9mQGRqPx%2BvMl4GV1rMVXT%2FazDtI1A2l%0AcX9r%2B%2FmNAygSTCkFOapIhIvMYxSNK4tn69PBc0RBfrLsB1CEIBPUsAXAg5bBbgwiQoQKQSQEg%2FaR%0AqBCkgyqSO322H99v3HnRWFvd%2Be3Pxmd%2F7HZxx3KIS5aTIgGBu1NJ5EnRwCOM9wJTUCLdmNpd3Jko%0AIo5QoqJAZHKHOs%2FMMIrW5qGvH1KpkpHRK7qROqwF65kqRMAsYv3APFNFgVH7SBTYBtPLoowxPwT1%0A7HbrwYPmd9dbD1f39dmVap89ICVzByiiMEUBA3eoS6Oz4wvjhoIoeRsBqTNyn3iwCbKafI97B%2FbO%0AwQcXHHeOipjKmAGWu%2BjkxHxy3hg1mD8ronuIfyXL41J6SzpMYhETKlHmtVYGLxTDhdjCCJJ8yVRf%0ANdxNom5Kdg%2BPBdQhpRAxJiIFAXemzIScDi%2FODTPu6xQ%2BKVOyK1PSmwlR6jgzIUISMHCHqi2JybGx%0A6QVI0v6fmV4zE2NGAMldsihH9RGRLRPkaxp70iE3w7op2T2OrQQDDnnVRpVzictqJYeknkjXVKlr%0AUit5KjlkIJaSjAHAXUlORyKxZCzOsNgTSl3Dl%2BodvmSXwYQoCLgzJQqp6bgh1wn1dTAdtcRmVlKr%0AqhYYA06ym%2BBaqNCAs6JFqCrWWejDIQkm3oGsdf2XnWu%2Ftx7eb%2F200vjh2s7NVU9WJiGH2hNgRVEB%0AM3dYIxcslMYmFjk73qqQPQmrVigcdMNWhRBU7YYqqLYbWFkNbCsdCl2NZ08bT7daK1uNm2uduzp%2F%0Ar1xt00CjXSNYjcdfNNZ%2BhsbOvY3m%2Bkpz%2FcfGxvrex7WbzW824SPUGo3rq1bD3u%2Bw%2FtTmr82vnjT%2B%0A%2BhrarXur%2F3y%2FYR2882L7yVbHiJYVx7kP1SwDVo%2B5X0L6xWo%2BJIm%2BrMhl%2BH6G2fkPcJvpI%2FxQVbY3%0AydsnX5ZjtvARcjkIhTLcqzuIbkakpdj0sD8F%2FvE8VIW6e7RPeniIsiQj2RFF4aJnMb90KWHO4LxG%0AsC%2FZxqsV8xI6zNRZzO%2F2cS%2FmEXWWIooMCO5Suel8RqLLkz7XnqdsLbU2PTwLy3AoHj5L5sIwF0%2Fh%0A9r6%2FS6nD4wCOJcfhZy2lQObuSjLZcJbGNYp8Ldi7724fr8RSpeOVWCdLiyUGTB4l1vSsGUWJBJJ7%0AosR6Y2mxQkDAI3vLTE0GjZkaQj1RPbS3HF%2F%2FriRU7AgI3J0uLE2NTmWXypi8404cGh5OpRHtbHzu%0AokYJ7gmnrjsbSe%2BdDWclIiIA8Hi8Mj9nJNCFs5T4EujtqsmftwfeTgUlUQz1q%2BMmuaRIoOyRHC%2FF%0AshPjBpdRbwzYNzSxqYwVIPBYTzkpGjiSp6IvqfH%2BIuJ0Jn4OZQeUpk7P72VEEAY3d9yZYk4crS8P%0AU%2B7LIDT1VO4juMtawewUVJHAQrtDkquDdksVuGTrIoHbcsGwwJF9KmpdAIEDToF0O4IweyQzVTic%0A07Tufrr9%2BPbg9tPPW1e%2F3Hm%2Bsf3X3ebVh83NG431u3uy%2B8PCwRxHcdqjQgRzCQOdu298MVS4XFy4%0AiPxNrE%2BeDB4hG%2BzykMfxsT%2FUzcgraa6OT7KFmfkEdHunnSQoganHeyQ5rarVzfAEob4Ew9P6fhtI%0AQd4MCO5SISWm51PRCUJ8HVG9V9La7wpKwOTxCCNZV5MsE6X%2BPH%2F1fPPUadNT%2FS%2BF9MaC4QWDzHPE%0AYYcNFOu9U4Ko13NVHE4uYXEyzuhp3Jh67W%2FnSvYeiLMUQ4Bw5cN%2FAVBLBwhWvm7qtwYAAMcsAAA%3D%0A; Hm_lpvt_838fbc4154ad87515435bf1e10023fab=1569201183'
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'WangFang.middlewares.WangfangSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'WangFang.middlewares.WangfangDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'WangFang.pipelines.KanqiPipeline': 300,
   #  'scrapy_redis.pipelines.RedisPipeline': 400,
}

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
MYSQL_HOST = ''
MYSQL_USER = ''
MYSQL_PASSWORD = ''
MYSQL_DB = 'wanfangproject'

# REDIS_PORT = '6379'
# REDIS_HOST = '127.0.0.1'
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# SCHEDULER = "scrapy_redis.scheduler.Scheduler"

SCHEDULER_PERSIST = True

# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"


