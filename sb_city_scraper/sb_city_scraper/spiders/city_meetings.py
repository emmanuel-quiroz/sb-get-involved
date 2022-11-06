import scrapy
from urllib.parse import urljoin
from sb_city_scraper.items import Meeting

class SbCitySpider(scrapy.Spider):
    name = 'city_meetings'
    start_urls = ['http://sanbernardinocityca.iqm2.com/Citizens/calendar.aspx']

    def parse(self, response):
        
        links = response.xpath('//*[@class="RowLink"]/a/@href').getall()
        base_url = 'http://sanbernardinocityca.iqm2.com'
        meeting_links = []


        for link in links:
            url = urljoin(base_url, link)
            yield scrapy.Request(url, callback=self.parse_meeting)

    def parse_meeting(self, response):
        meeting = Meeting()
        meeting['Groups'] = response.xpath('//*[@id="ContentPlaceholder1_lblMeetingGroup"]/text()').get()
        meeting['Type'] = response.xpath('//*[@id="ContentPlaceholder1_lblMeetingType"]/text()').get()
        date_time = response.xpath('//*[@id="ContentPlaceholder1_lblMeetingDate"]/text()').get().split()
        meeting['Date'] = date_time[0]
        meeting['Time'] = date_time[1] + ' ' + date_time[2]
        meeting['Location']  = response.xpath('//*[@class="MeetingAddress"]/text()').get()
        meeting['Info'] = response.request.url

        return meeting 
        


            
        