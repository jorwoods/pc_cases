import scrapy
import re

HTML_TAGS = re.compile("<.*?>")
base_url = 'https://www.newegg.com/p/pl?N=100007583%20601310882&page={}'


class NeweggSpider(scrapy.Spider):
    name = 'newegg'
    allowed_domains = ['www.newegg.com']
    start_urls = [base_url.format(i) for i in range(1, 14)]

    def parse(self, response):
        items = response.css("div.item-container a.item-img::attr(href)")
        yield from response.follow_all(items, self.parse_case)

    def parse_case(self, response):
        def extract_with_css(item, query):
            return HTML_TAGS.sub("", item.css(query).get(default='')).strip()

        title = extract_with_css(response, "head title")

        # if "are you a human" in title.lower():
        #     raise CloseSpider("Bot was detected")

        data = {}
        for row in response.css("div#product-details.tab-box tr"):
            data[extract_with_css(row, "th").lower()] = extract_with_css(row, "td")

        data['price'] = extract_with_css(response, "div.product-pane ul.price li.price-current strong")
        data['name'] = title
        data["url"] = response.url

        yield data
