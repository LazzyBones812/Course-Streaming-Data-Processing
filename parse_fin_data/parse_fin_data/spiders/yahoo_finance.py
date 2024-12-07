import scrapy
from confluent_kafka import Producer

class YahooFinanceSpider(scrapy.Spider):

    name = 'yahoo_finance'
    allowed_domains = ["finance.yahoo.com"]
    start_urls = ["https://finance.yahoo.com/quote/AMZN/news/"]
    lst = ['AMZN', 'APPL', 'TSLA', 'NVDA', 'INTC', 'GOOG', 'META', 'MSFT', 'AMD', 'TSM']
    start_urls = ['https://finance.yahoo.com/quote/' + x + '/news/' for x in lst]

    TOPIC_NAME = "some_topic"
    producer = Producer({"bootstrap.servers": "kafka:29092"})

    def parse(self, response):
        for url_content in response.xpath("//li[@class = 'stream-item story-item yf-1usaaz9']/section/a"):
            self.producer.produce(self.TOPIC_NAME, 
                                  key = response.xpath("//h1[@class = 'yf-xxbei9']/text()").get(), 
                                  value = url_content.xpath('@title').get())
            self.producer.flush()

            yield {'title' : url_content.xpath('@title').get(), 'describe' : response.xpath("//p[@class = 'clamp  yf-1n6s2tt']/text()").get(),
                   'header' : response.xpath("//h1[@class = 'yf-xxbei9']/text()").get()}
