# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from typing import Dict
from itemadapter import ItemAdapter
import re

measurement = re.compile(r"(?P<size>[\d\.]+)\s*(?P<unit>in|mm)?|$")
dimension_order = re.compile(r"\(([hwld])\s*x\s*([hwld])\s*x\s*([hwld])")
hwd = {'h': 'height', 'w':'width', 'd':'depth', 'l': 'depth'}

def cast_float(x):
    if x is None:
        return None
    else:
        return float(re.sub(r"[^\d\.]", "", x))

class PcCasesPipeline:
    def process_item(self, item, spider):

        item.update(self.parse_dimensions(item))
        item.update(self.parse_gpu(item))
        
        return item

    def parse_dimensions(self, page_specs: Dict[str, str]) -> Dict[str, str]:
        data = {}
        for key in page_specs.keys():
            if not key.startswith("dimension"):
                continue
            order = dimension_order.findall(key)
            if order:
                dim_order = [hwd[i] for i in order[0]]
            else:
                dim_order = ['height', 'width', 'depth']
            
            regex = re.compile(r"""
                    (?P<{0}>[\d\.]+)
                    \s*("|mm)?\s*([x\*])\s*
                    \s*(?P<dim_label_0>\([LWHD]\))?
                    (?P<{1}>[\d\.]+)
                    \s*("|mm)?\s*([x\*])\s*
                    \s*(?P<dim_label_1>\([LWHD]\))?
                    (?P<{2}>[\d\.]+)
                    \s*(?P<dim_label_2>\([LWHD]\))?
                    \s*
                    (?P<unit>mm|in|")?
                    |$ # Regex capture no matches so groupdict doesn't error.
                """.format(*dim_order), re.VERBOSE | re.IGNORECASE)

            parsed = regex.search(page_specs[key]).groupdict()
            if any((parsed[k] is not None for k in dim_order)):
                if parsed['dim_label_0'] is not None:
                    parsed.update(
                        {hwd[parsed[f'dim_label_{i}'].lower()[1]]: parsed[dim_order[i]]
                        for i in range(3)}
                    )
                data['height'] = cast_float(parsed['height'])
                data['width'] = cast_float(parsed['width'])
                data['depth'] = cast_float(parsed['depth'])
                data['units'] = parsed['unit']
                if data['units'] == '"':
                    data['units'] == 'in'

                return data

    def parse_gpu(self, page_specs: Dict[str, str]) -> Dict[str, float]:
        gpu = {}
        for key in page_specs:
            if not any(x in key for x in ('gpu', 'video', 'gfx')):
                continue
            gpu_info = measurement.search(page_specs[key].lower()).groupdict()
            if gpu_info['size'] is None:
                continue
            size = cast_float(gpu_info['size'])
            multiple = 1
            if gpu_info['unit'] == 'in' or size < 30:
                multiple = 25.4
            
            gpu['max_gpu_length'] = size * multiple

            return gpu
