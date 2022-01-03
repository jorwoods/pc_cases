import scrapy
import re

HTML_TAGS = re.compile("<.*?>")


class CoolermasterSpider(scrapy.Spider):
    name = 'coolermaster'
    allowed_domains = ['https://www.coolermaster.com']
    start_urls = ['https://www.coolermaster.com/catalog/cases/?filter=8448/#!/Size=Mid%20Tower']

    def parse(self, response):
        cases = response.css("div.card__img a::attr(href)")
        yield from response.follow_all(cases, self.parse_case)

    def parse_case(self, response):
        def extract_with_css(item, query):
            return HTML_TAGS.sub("", item.css(query).get(default='')).strip()

        
