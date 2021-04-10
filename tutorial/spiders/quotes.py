import scrapy
from tutorial.items import TutorialItem

class QuotesSpider(scrapy.Spider):

    # Spider类
    name = 'quotes'  # 爬虫的名字
    allowed_domains = ['quotes.toscrape.com'] # 可选配置，不在此列的链接不会被跟进爬取
    start_urls = ['http://quotes.toscrape.com/'] # 起始URL
    # custom_settings =   # 是一个字典，专属于本Spider的配置，设置会覆盖全局设置，必须在初始化前更新，必须定义成类变量
    # crawler =           # 是在pipeline.py的from_crawler() 方法设置的，代表的是本Spider类对应的Crawler对象，可以用来获取setting的信息
    # settings 全局设定
    # start_requests()用于生成初始请求，必须返回一个可迭代对象，默认使用Get方法。如果想使用Post方法，只需要重写这个方法，发送POST请求时使用FormRequest即可
    # parse() 当Response没有指定回调函数时，本方法默认被调用，负责处理Response，处理返回结果，需要返回一个包含Request和Item的可迭代对象
    # close() 释放资源

    def parse(self, response):
        quotes = response.css('.quote')

        for quote in quotes:
            item = TutorialItem()
            item['text'] = quote.css('.text::text').extract_first()
            item['author'] = quote.css('.author::text').extract_first()
            item['tags'] = quote.css('.tags .tag::text').extract()
            yield item
            
        next = response.css('.pager .next a::attr("href")').extract_first()
        url = response.urljoin(next)
        yield scrapy.Request(url=url,callback = self.parse)
        	
