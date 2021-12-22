import scrapy
import re

divs = re.compile(r"<div.*?>(.*)</div>")

class MicrocenterSpider(scrapy.Spider):
    name = 'microcenter'
    allowed_domains = ['microcenter.com']
    start_urls = ['https://www.microcenter.com/category/4294964318/desktop-cases/']


    def parse(self, response):
        try:
            page_num = re.findall(r"page=(\d+)", response.url)[0]
        except IndexError:
            page_num = "1"
        filename = f"microcenter-cases-{page_num}.html"
        with open(filename, "wb") as f:
            f.write(response.body)

        cases = response.css("li.product_wrapper div.result_left a.image::attr(href)")
        yield from response.follow_all(cases, self.parse_case)

        next_page = response.css("div#bottomPagination ul.pages.inline li:last-child a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    
    def parse_case(self, response, ):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()
        def remove_divs(s):
            return ' '.join(divs.findall(s))
        
        data = response.css("div.spec-body div").getall()
        data = [remove_divs(d) for d in data]
        data = dict(zip(data[::2], data[1::2]))

        data['price'] = extract_with_css("div#options-pricing span#pricing::attr(content)")
        data['name'] = extract_with_css("title::text")
        data["url"] = response.url
        yield data        
