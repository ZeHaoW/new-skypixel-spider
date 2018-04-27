import scrapy
import json
from scrapy import Request
from new_skypixel.items import NewSkypixelItem

class SkypixelSpider(scrapy.Spider):
    name = "new_skypixel"
    count = 1
    start_urls = ["https://www.skypixel.com/api/website/tags/4d10645e-685b-4a64-a4b5-57763a911f71?page=%s"]
    # ITEM_PIPELINES = {'skypixel_spider.pipelines.SkypixelPhotosPipeline': 1}
    # IMAGE_EXPIRES = 90

    def parse(self, response):
        item = NewSkypixelItem()
        item['image_urls'] = []
        jsonObj = json.loads(response.body_as_unicode())
        jars = jsonObj['photos']
        for n in jars:
            photo_url = n['image'] + '@!1200'
            item['image_urls'].append(photo_url)
        self.count+=1
        yield item
        yield Request(url=self.start_urls[0] % str(self.count), callback=self.parse)

    def start_requests(self):
        yield Request(url=self.start_urls[0] % str(self.count), callback=self.parse)
