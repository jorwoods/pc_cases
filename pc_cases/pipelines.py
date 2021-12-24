# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re

measurement = re.compile(r"(?P<size>[\d\.]+)\s*(?P<unit>in|mm)?|$")

def cast_float(x):
    if x is None:
        return None
    else:
        return float(x)

class PcCasesPipeline:
    def process_item(self, item, spider):
        for key in item.keys():
            if not any(x in key for x in ('gpu', 'video')):
                continue
            gpu_info = measurement.search(item[key].lower()).groupdict()
            if gpu_info['size'] is None:
                continue
            size = cast_float(gpu_info['size'])
            multiple = 1
            if gpu_info['unit'] == 'in' or size < 30:
                multiple = 25.4
            
            item['max_gpu_length'] = size * multiple
        return item
