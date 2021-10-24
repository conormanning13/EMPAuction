# -*- coding: utf-8 -*-
import scrapy


class EMPAuctionSpider(scrapy.Spider):
    name = 'auction'
    allowed_domains = ['www.emovieposter.com']
    start_urls = [
        'http://www.emovieposter.com/agallery/page/1/16.html']

    def parse(self, response):

        for result in response.xpath('//table[@class="gallery"]/tr/td'):
            yield {
                'title': result.xpath('./div/a[1]/text()').get()[7:],
                'lot_number': result.xpath('./div/a[1]/text()').get()[:6],
                'price': result.xpath('./div/font/b/text()').get(),
                'high_bidder': result.xpath('./div/span[2]/b/text()').get(),
                'item_number': result.xpath('./div/a[1]/@href').get().split('=')[-1],
                'page': response.url.split('/')[-2]
            }
        page_links = response.xpath('//*[@id="main-content-center"]/div[1]/center[3]/div[2]/span')
        last_page = page_links.xpath('./a[14]/@href').extract_first()
        number_of_pages = int(last_page.split('/')[-2])

        for page in range(2, number_of_pages+1):
            next_page = f'http://www.emovieposter.com/agallery/page/{page}/16.html'
            yield response.follow(next_page, callback=self.parse)
