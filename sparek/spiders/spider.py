import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import SparekItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class SparekSpider(scrapy.Spider):
	name = 'sparek'
	start_urls = ['https://www.sparekassen.dk/Sparekassen/Nyheder']

	def parse(self, response):
		post_links = response.xpath('//div[@class="modulelayout2717_2"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = "Unknown"
		title = response.xpath('//div[@class="vdcontent"]/h2/text()').get()
		content = response.xpath('//div[@class="vdcontent"]/p//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=SparekItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
