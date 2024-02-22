import scrapy
from scrapy_dangdang_tushu.items import ScrapyDangdangTushuItem

class DdtsSpider(scrapy.Spider):
    name = "ddts"
    allowed_domains = ["category.dangdang.com"]
    start_urls = ["http://category.dangdang.com/cp01.01.02.00.00.00.html"]

    base_url = "http://category.dangdang.com/pg"
    page = 1
    def parse(self, response):
        # src = //a[@name='itemlist-picture']/img/@src
        # name = //a[@name='itemlist-picture']/img/@alt
        # price = //span[@class='search_now_price']/text()
        li_list = response.xpath("//ul[@id='component_59']/li")

        for li in li_list:
            src = li.xpath(".//img/@data-original").extract_first()
            # 处理懒加载
            # 第一张图片无data-original属性，所以用src属性代替
            if src :
                src = src 
            else :
                src = li.xpath(".//img/@src").extract_first()
            name = li.xpath(".//img/@alt").extract_first()
            price = li.xpath(".//span[@class='search_now_price']/text()").extract_first()

            # print(src,name,price)
            book = ScrapyDangdangTushuItem()
            book['src'] = src
            book['name'] = name
            book['price'] = price

            yield book

        # if self.page < 1:
        #     self.page += 1
        #     url = self.base_url + str(self.page) + "-cp01.01.02.00.00.00.html"
        #     yield scrapy.Request(url=url, callback=self.parse)