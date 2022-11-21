import scrapy
from scrapy.http import HtmlResponse
from urllib.parse import urljoin
from sb_city_scraper.items import NewsItem


class PoliceNewsSpider(scrapy.Spider):
    name = 'police_news'
    start_urls = ['https://www.sbcity.org/city_hall/police_department/press_releases']


    def parse(self, response):
        base_url = 'https://cdn5-hosted.civiclive.com'

        # retrieve all divs containing relevant content 
        news_summary = response.xpath('//*[@id="news-summary"]/div/*[@class="content"]').getall()
        
        for k in news_summary:
            # Cast str html into HtmlResponse object for data manipulation
            response = HtmlResponse(url='', body=k, encoding='utf-8')   

            news_item = NewsItem()
            news_item['Title'] = response.xpath('//a[@class="title"]/@title').get()
            news_item['Date'] = response.xpath('//div[@class="date"]/text()').get()
            news_item['Desc'] = response.xpath('//div[@class="summary"]/text()').get()
            news_item['Read_more'] = base_url + response.xpath('//a[@class="read-more"]/@href')[1].get()
             
            yield news_item