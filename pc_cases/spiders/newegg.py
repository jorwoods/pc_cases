import scrapy
import re
from scrapy.exceptions import CloseSpider

HTML_TAGS = re.compile("<.*?>")
base_url = 'https://www.newegg.com/p/pl?N=100007583%20601310882&page={}'
dimension_order = re.compile(r"\(([hwld])\s*x\s*([hwld])\s*x\s*([hwld])")
hwd = {'h': 'height', 'w':'width', 'd':'depth', 'l': 'depth'}

def cast_float(x):
    if x is None:
        return None
    else:
        return float(x)

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
        data['name'] = extract_with_css(response, "head title")
        data["url"] = response.url
        
        for key in data.keys():
            if not key.startswith("dimension"):
                continue
            order = dimension_order.findall(key)
            if order:
                dim_order = [hwd[i] for i in order[0]]
            else:
                dim_order = ['height', 'width', 'depth']

            regex = re.compile(r"""
                (?P<{0}>[\d\.]+)
                \s*(\([LWHD]\))?
                \s*("|mm)?\s*x\s*
                (?P<{1}>[\d\.]+)
                \s*(\([LWHD]\))?
                \s*("|mm)?\s*x\s*
                (?P<{2}>[\d\.]+)
                \s*(\([LWHD]\))?
                \s*
                (?P<unit>mm|in|")?|$
            """.format(*dim_order), re.VERBOSE | re.IGNORECASE)
            parsed = regex.search(data[key]).groupdict()
            if any((v is not None for v in parsed.values())):
                data['height'] = cast_float(parsed['height'])
                data['width'] = cast_float(parsed['width'])
                data['depth'] = cast_float(parsed['depth'])
                data['units'] = parsed['unit']
                if data['units'] == '"':
                    data['units'] == 'in'
                break

        yield data
